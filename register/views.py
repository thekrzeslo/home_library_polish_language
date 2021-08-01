from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import logout, login, authenticate



def login_view(request):

    form = AuthenticationForm(data=request.POST or None)
    form.fields['username'].label = 'Nazwa użytkownika'
    form.fields['password'].label = 'Hasło'
    form.error_messages['invalid_login'] = 'Wprowadź poprawną nazwę użytkownika i hasło. Pamiętaj, że w obu polach może być rozróżniana wielkość liter.'
    form.error_messages['inactive'] = 'To konto jest nieaktywne.'

    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(request, username=username, password=password)
        login(request, user)
        return redirect('/')

    return render(request, 'registration/login.html', {'form': form})

def register_view(request):
    form = UserCreationForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('/')

    if "username" in form.errors:
        if "A user" in form.errors["username"].as_text():
            form.errors["username"][0] = "Użytkownik o tej nazwie już istnieje."

    if "password2" in form.errors:
        count = 0

        if "similar" in form.errors["password2"].as_text():
            form.errors["password2"][count] = "Hasło jest zbyt podobne do nazwy użytkownika."
            count += 1

        if "short" in form.errors["password2"].as_text():
            form.errors["password2"][count] = "To hasło jest za krótkie. Musi zawierać co najmniej 8 znaków."
            count += 1

        if "common" in form.errors["password2"].as_text():
            form.errors["password2"][count] = "To hasło jest zbyt powszechne."
            count += 1

        if "numeric" in form.errors["password2"].as_text():
            form.errors["password2"][count] = "To hasło jest całkowicie numeryczne."
            count += 1

    form.error_messages['password_mismatch'] = 'Dwa pola hasła nie pasują do siebie.'
    form.fields['username'].label = 'Nazwa użytkownika'
    form.fields['username'].help_text = 'Wymagane: 150 znaków lub mniej. Tylko litery, cyfry i @/./+/-/_'
    form.fields['password1'].label = 'Hasło'
    form.fields['password1'].help_text = '<ul><li>Twoje hasło nie może być zbyt podobne do innych Twoich danych osobowych.</li><li>Twoje hasło musi zawierać co najmniej 8 znaków.</li><li>Twoje hasło może nie może być powszechnie używanym hasłem.</li><li>Twoje hasło nie może być całkowicie numeryczne.</li></ul>'
    form.fields['password2'].label = 'Powtórz Hasło'
    form.fields['password2'].help_text = 'Wprowadź to samo hasło co poprzednio, w celu weryfikacji.'


    return render(request, 'register/register.html', {'form': form})




def logout_view(request):
    logout(request)
    return redirect('login')