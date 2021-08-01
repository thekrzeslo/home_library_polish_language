from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from .models import Books
from .forms import BooksForm
from django.views import View


from requests_html import requests

from bs4 import BeautifulSoup
import requests
from requests_html import HTMLSession


import openpyxl


def get_source(url):
    try:
        session = HTMLSession()
        response = session.get(url)
        return response

    except requests.exceptions.RequestException as e:
        print(e)


def get_results(query):

    query = "+".join(query.split())
    response = get_source("https://www.google.com/search?q=" + query)

    return response


def parse_results(response):
    css_identifier_result = ".wDYxhc"
    css_identifier_description = ".LGOjhe span"
    results = response.html.find(css_identifier_result)

    for i in results:
        try:
            output = i.find(css_identifier_description, first=True).text
            break
        except:
            continue
    else:
        output = ""

    return output

def google_search(query):
    response = get_results(query)
    return parse_results(response)


def save_as_lxml(queryset):
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet["A1"] = "Tytuł"
    sheet["B1"] = "Autor"
    sheet["C1"] = "Gatunek"

    sheet_title_num = 2
    sheet_author_num = 2
    sheet_type_num = 2

    for i in queryset:

        sheet["A" + str(sheet_title_num)] = i.title
        sheet["B" + str(sheet_author_num)] = i.author
        sheet["C" + str(sheet_type_num)] = i.type
        sheet_title_num += 1
        sheet_author_num += 1
        sheet_type_num += 1


    workbook.save("static/data/books_data.xlsx")




class BookListView(View):
    template_name = 'books/books_list.html'
    queryset = None
    collapse_switch = "collapse"

    title_value = ""
    author_value = ""
    description_value = ""
    type_value = ""

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/login')

        filtr = {"user":request.user}

        temp = request.GET


        for k, v in temp.items():
            if v:
                filtr[k + "__contains"] = v


        if filtr:
            self.queryset = Books.objects.filter(**filtr)

        books_counter = len(self.queryset)

        content = {
            "object_list" : self.queryset,
            "books_counter" : books_counter,
        }

        content["collapse_switch"] = self.collapse_switch

        return render(request, self.template_name, content)


    def post(self, request, *args, **kwargs):
        filtr = {"user" : request.user}

        if request.POST.get("create"):
            form = BooksForm(request.POST)

            if form.is_valid():
                form.instance.user = request.user
                form.save()
                self.queryset = Books.objects.filter(**filtr)

            save_as_lxml(self.queryset)

        elif request.POST.get("update"):
            filtr = {"user":request.user}

            id = request.POST.get("update")

            obj = get_object_or_404(Books, id=id)

            form = BooksForm(request.POST, instance=obj)

            if form.is_valid():
                form.instance.user = request.user
                form.save()
                self.queryset = Books.objects.filter(**filtr)


            save_as_lxml(self.queryset)


        elif request.POST.get("delete"):
            filtr = {"user":request.user}

            id  = request.POST.get("delete")

            obj = get_object_or_404(Books, id=id)

            if obj:
                obj.delete()
                self.queryset = Books.objects.filter(**filtr)

            save_as_lxml(self.queryset)

        elif request.POST.get("autofill"):
            book_name = request.POST["title"]

            if book_name:
                url = "https://lubimyczytac.pl/szukaj/ksiazki?phrase=" + book_name

                html_text = requests.get(url).text

                soup = BeautifulSoup(html_text, 'html.parser')

                try:
                    book = soup.find("div", class_="authorAllBooks__single")

                    a = book.find("a", class_="authorAllBooks__singleTextTitle float-left")

                    link = a["href"]

                    url = "https://lubimyczytac.pl" + link

                    html_text = requests.get(url).text

                    soup = BeautifulSoup(html_text, 'html.parser')

                    book_name = soup.find("h1", class_="book__title js-book-title-scale").text.strip()

                    book_author = soup.find("a", class_="link-name").text

                    book_type = soup.find("a", class_="book__category d-sm-block d-none").text.strip()

                except:
                    book_author = ""
                    book_type = ""

                description = google_search(book_name + " opis książki")


                self.title_value = book_name
                self.author_value = book_author
                self.description_value = description
                self.type_value = book_type

            filtr = {"user" : request.user}

            self.collapse_switch = "collapse show"

            self.queryset = Books.objects.filter(**filtr)

        elif request.POST.get("reset"):
            book_name = request.POST["title"]

            self.title_value = book_name
            self.author_value = ""
            self.description_value = ""
            self.type_value = ""

            filtr = {"user":request.user}

            self.collapse_switch = "collapse show"

            self.queryset = Books.objects.filter(**filtr)

        books_counter = len(self.queryset)

        content = {
            "object_list" : self.queryset,
            "books_counter"  : books_counter,
            "title_value" : self.title_value,
            "author_value" : self.author_value,
            "description_value" : self.description_value,
            "type_value" : self.type_value,
        }

        content["collapse_switch"] = self.collapse_switch

        return render(request, self.template_name, content)





