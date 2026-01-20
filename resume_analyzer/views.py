from django.shortcuts import render, redirect, get_object_or_404
from .models import Resume
from .forms import ResumeUploadForm
from ai.resume_parser import extract_text_from_pdf
from ai.skill_extractor import extract_skills
from ai.job_predictor import predict_job_role, get_missing_skills
from ai.scorer import calculate_score, get_improvement_suggestions
import os
from django.conf import settings

def upload_resume(request):
    if request.method == 'POST':
        form = ResumeUploadForm(request.POST, request.FILES)
        if form.is_valid():
            resume = form.save()
            
            # Process AI
            file_path = resume.file.path
            
            # 1. Extract Text
            # Update: Unpack the tuple (text, error)
            text, extract_error = extract_text_from_pdf(file_path)
            
            if text:
                # 2. Extract Skills
                skills = extract_skills(text)
                
                # 3. Predict Role
                role, confidence = predict_job_role(text)
                
                # 4. Get Missing Skills
                missing_skills = get_missing_skills(role, skills)
                
                # 5. Calculate Score
                score = calculate_score(text, skills, role)
                
                # Save results
                resume.predicted_role = role
                resume.confidence_score = confidence
                resume.score = score
                resume.extracted_skills = skills
                resume.recommended_skills = missing_skills
                resume.save()
                
                return redirect('resume_result', pk=resume.pk)
            else:
                # Handle error if text extraction failed
                resume.delete()
                # Use the specific error message returned from parser
                error_msg = extract_error if extract_error else "Could not extract text from PDF. Unknown error."
                return render(request, 'upload.html', {'form': form, 'error': error_msg})
    else:
        form = ResumeUploadForm()
    
    return render(request, 'upload.html', {'form': form})

def resume_result(request, pk):
    resume = get_object_or_404(Resume, pk=pk)
    
    # Also handle extraction here just in case, though usually we rely on stored data
    # But since we don't store text, we re-extract.
    text, _ = extract_text_from_pdf(resume.file.path)
    
    if not text:
         # Fallback if somehow re-extraction fails (unlikely if it passed first time)
         text = ""
         
    suggestions = get_improvement_suggestions(text, resume.extracted_skills, resume.score)
    
    context = {
        'resume': resume,
        'suggestions': suggestions
    }
    return render(request, 'result.html', context)

def dashboard(request):
    resumes = Resume.objects.all().order_by('-uploaded_at')
    
    # Simple Analytics
    total_resumes = resumes.count()
    roles = {}
    for r in resumes:
        if r.predicted_role:
            roles[r.predicted_role] = roles.get(r.predicted_role, 0) + 1
            
    context = {
        'resumes': resumes,
        'total_resumes': total_resumes,
        'role_distribution': roles
    }
    return render(request, 'dashboard.html', context)
