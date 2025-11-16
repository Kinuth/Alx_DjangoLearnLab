from django import forms
import bleach

class SearchForm(forms.Form):
    """
    A form for searching books.
    This form handles validation and sanitization of user input.
    """
    query = forms.CharField(
        max_length=100,
        required=True,
        label="Search",
        # Django's CharField (and forms system) is the first line
        # of defense against XSS and other bad input.
    )

    def clean_query(self):
        """
        Custom cleaning method for the 'query' field.
        """
        query_data = self.cleaned_data.get('query')

        # Step 3: Sanitize input
        # Use a library like 'bleach' to strip out any
        # malicious HTML tags if you plan to render this
        # query back to the user.
        # Run: pip install bleach
        sanitized_query = bleach.clean(query_data, tags=[], strip=True)
        
        # Example validation: ensure query isn't just whitespace
        if not sanitized_query.strip():
            raise forms.ValidationError("Please enter a valid search term.")

        return sanitized_query