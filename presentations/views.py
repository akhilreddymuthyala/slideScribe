from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods

from .models import Presentation
from .forms import PresentationUploadForm
from parser_engine.services import parse_document, ParserError


@login_required
def dashboard(request):
    presentations = Presentation.objects.filter(user=request.user)
    context = {
        'presentations': presentations,
        'total': presentations.count(),
        'ready': presentations.filter(status='READY').count(),
        'recent': presentations[:6],
    }
    return render(request, 'dashboard.html', context)


@login_required
@require_http_methods(["GET", "POST"])
def create_presentation(request):
    if request.method == 'POST':
        form = PresentationUploadForm(request.POST, request.FILES)
        if form.is_valid():
            presentation = form.save(commit=False)
            presentation.user = request.user
            presentation.status = 'UPLOADED'
            presentation.save()

            presentation.status = 'PARSING'
            presentation.save(update_fields=['status'])

            try:
                uploaded_file = presentation.uploaded_file
                raw_text = form.cleaned_data.get('raw_text', '').strip()

                if uploaded_file:
                    uploaded_file.open('rb')
                    parsed = parse_document(file_obj=uploaded_file, filename=uploaded_file.name)
                    uploaded_file.close()
                elif raw_text:
                    parsed = parse_document(raw_text=raw_text)
                else:
                    raise ParserError("No content provided to parse.")

                presentation.parsed_content = parsed
                presentation.raw_text = parsed.get('raw_text', '')[:50000]

                if not presentation.title:
                    presentation.title = parsed.get('title', 'Untitled Presentation')

                presentation.status = 'UPLOADED'
                presentation.save()

                messages.success(
                    request,
                    f"'{presentation.title}' parsed successfully — "
                    f"{parsed.get('word_count', 0)} words, "
                    f"{len(parsed.get('sections', []))} sections detected."
                )
                return redirect('presentation_detail', pk=presentation.pk)

            except ParserError as e:
                presentation.status = 'ERROR'
                presentation.save(update_fields=['status'])
                messages.error(request, f"Parsing failed: {e}")
                return redirect('presentation_detail', pk=presentation.pk)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
    else:
        form = PresentationUploadForm()

    return render(request, 'presentations/create.html', {'form': form})


@login_required
def presentation_detail(request, pk):
    presentation = get_object_or_404(Presentation, pk=pk, user=request.user)
    return render(request, 'presentations/detail.html', {'presentation': presentation})


@login_required
@require_http_methods(["POST"])
def delete_presentation(request, pk):
    presentation = get_object_or_404(Presentation, pk=pk, user=request.user)
    title = presentation.title
    presentation.delete()
    messages.success(request, f"'{title}' deleted.")
    return redirect('dashboard')