from django import forms
from .models import Presentation, PRESENTATION_TYPES, AUDIENCE_TYPES

ALLOWED_EXTENSIONS = ['pdf', 'docx', 'md', 'markdown', 'txt']
MAX_FILE_SIZE_MB = 20


class PresentationUploadForm(forms.ModelForm):
    title = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'ss-input',
            'placeholder': 'e.g. Real-Time Sign Language Detection',
        }),
    )
    raw_text = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'ss-input',
            'rows': 8,
            'placeholder': 'Paste your notes, outline, or draft content here...',
        }),
    )

    class Meta:
        model = Presentation
        fields = ['title', 'presentation_type', 'audience', 'uploaded_file', 'raw_text']
        widgets = {
            'presentation_type': forms.Select(attrs={'class': 'ss-input ss-select'}),
            'audience': forms.Select(attrs={'class': 'ss-input ss-select'}),
        }

    def clean(self):
        cleaned = super().clean()
        uploaded_file = cleaned.get('uploaded_file')
        raw_text = cleaned.get('raw_text')

        if not uploaded_file and not raw_text:
            raise forms.ValidationError(
                "Upload a file (PDF, DOCX, README.md) or paste raw notes."
            )

        if uploaded_file:
            ext = uploaded_file.name.rsplit('.', 1)[-1].lower() if '.' in uploaded_file.name else ''
            if ext not in ALLOWED_EXTENSIONS:
                raise forms.ValidationError(
                    f"Unsupported file type '.{ext}'. Allowed: PDF, DOCX, MD, TXT."
                )
            if uploaded_file.size > MAX_FILE_SIZE_MB * 1024 * 1024:
                raise forms.ValidationError(
                    f"File too large. Maximum size is {MAX_FILE_SIZE_MB}MB."
                )

        return cleaned