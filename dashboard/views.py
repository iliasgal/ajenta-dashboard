from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import UserForm, AdminForm
from .queries import *
from .graphs import generate_graph, generate_pie_chart
from .models import Call
from datetime import datetime

# Dictionary of reports and the equivalent view functions
report_dict = {
    'User Stats': 'user_stats',
    'Room Stats': 'room_stats',
    'Calls per day': 'calls_per_day',
    'Maximum concurrent lines': 'concurrent_lines',
    'Calls by country': 'calls_by_country',
    'Platform Stats': 'platform_stats',
    'OS Stats': 'os_stats'
}


@login_required
def index(request):
    if request.method == 'POST':
        if request.user.is_superuser:
            form = AdminForm(request.POST)
            form.fields['tenant'].choices = get_tenants()
            request.session['username'] = request.POST.get('tenant')
        else:
            form = UserForm(request.POST)
            request.session['username'] = request.user.username

        if form.is_valid():
            if request.session['username'] in Call.objects.using('ajenta_io').values_list('tenantname',
                                                                                          flat=True).distinct():
                request.session['selected_db'] = 'ajenta_io'
            elif request.session['username'] == "All - ajenta.io":
                request.session['selected_db'] = 'ajenta_io'
                request.session['username'] = "All"
            elif request.session['username'] == "All - platformc":
                request.session['selected_db'] = 'platformc'
                request.session['username'] = "All"
            else:
                request.session['selected_db'] = 'platformc'

            # Redirect to the right view function, based on the button pressed
            try:
                requested_report = report_dict[request.POST['report']]
                request.session['start_date'] = request.POST.get('start_date')
                request.session['end_date'] = request.POST.get('end_date')
            except Exception as exception:
                print exception
            return redirect(requested_report)
    else:
        if request.user.is_superuser:
            form = AdminForm()
            form.fields['tenant'].choices = get_tenants()
        else:
            form = UserForm()

        try:
            form.fields['start_date'].initial = datetime.strptime(request.session['start_date'], '%d/%m/%Y')
            form.fields['end_date'].initial = datetime.strptime(request.session['end_date'], '%d/%m/%Y')
            form.fields['tenant'].initial = request.session['username']
        except (AssertionError, KeyError):
            pass

    return render(request, 'index.html', {'form': form})


@login_required
def user_stats(request):
    users = calculate_user_stats(request.session['username'], request.session['selected_db'],
                                 datetime.strptime(request.session['start_date'], '%d/%m/%Y'),
                                 datetime.strptime(request.session['end_date'], '%d/%m/%Y'))

    title = '10 most active users'
    (ids, graph_json) = generate_graph(users, title, request.session['username'], request.session['start_date'],
                                       request.session['end_date'])

    return render(request, 'stats/user_stats.html', {'ids': ids, 'graph_json': graph_json})


@login_required
def room_stats(request):
    rooms = calculate_room_stats(request.session['username'], request.session['selected_db'],
                                 datetime.strptime(request.session['start_date'], '%d/%m/%Y'),
                                 datetime.strptime(request.session['end_date'], '%d/%m/%Y'))

    title = '10 most active rooms'
    (ids, graph_json) = generate_graph(rooms, title, request.session['username'], request.session['start_date'],
                                       request.session['end_date'])

    return render(request, 'stats/room_stats.html', {'ids': ids, 'graph_json': graph_json})


@login_required
def calls_per_day(request):
    calls = calculate_calls_per_day(request.session['username'], request.session['selected_db'],
                                    datetime.strptime(request.session['start_date'], '%d/%m/%Y'),
                                    datetime.strptime(request.session['end_date'], '%d/%m/%Y'))

    title = 'Calls per day'
    (ids, graph_json) = generate_graph(calls, title, request.session['username'], request.session['start_date'],
                                       request.session['end_date'])

    return render(request, 'stats/calls_per_day.html', {'ids': ids, 'graph_json': graph_json})


@login_required
def concurrent_lines(request):
    lines = calculate_concurrent_lines(request.session['username'], request.session['selected_db'],
                                       datetime.strptime(request.session['start_date'], '%d/%m/%Y'),
                                       datetime.strptime(request.session['end_date'], '%d/%m/%Y'))

    title = 'Maximum concurrent lines'
    (ids, graph_json) = generate_graph(lines, title, request.session['username'], request.session['start_date'],
                                       request.session['end_date'])

    return render(request, 'stats/concurrent_lines.html', {'ids': ids, 'graph_json': graph_json})


@login_required
# @allowed_tenant('ActionAid')
def calls_by_country(request):
    countries = calculate_calls_by_country(request.session['username'], request.session['selected_db'],
                                           datetime.strptime(request.session['start_date'], '%d/%m/%Y'),
                                           datetime.strptime(request.session['end_date'], '%d/%m/%Y'))

    title = 'Calls per country'
    (ids, graph_json) = generate_graph(countries, title, request.session['username'], request.session['start_date'],
                                       request.session['end_date'])

    return render(request, 'stats/calls_by_country.html', {'ids': ids, 'graph_json': graph_json})


@login_required
def platform_stats(request):
    platforms = calculate_platform_stats(request.session['username'], request.session['selected_db'],
                                         datetime.strptime(request.session['start_date'], '%d/%m/%Y'),
                                         datetime.strptime(request.session['end_date'], '%d/%m/%Y'))

    title = 'Vidyo Platform stats'
    (ids, graph_json) = generate_pie_chart(platforms, title, request.session['username'], request.session['start_date'],
                                       request.session['end_date'])

    return render(request, 'stats/platform_stats.html', {'ids': ids, 'graph_json': graph_json})


@login_required
def os_stats(request):
    os = calculate_os_stats(request.session['username'], request.session['selected_db'],
                            datetime.strptime(request.session['start_date'], '%d/%m/%Y'),
                            datetime.strptime(request.session['end_date'], '%d/%m/%Y'))

    title = 'OS stats'
    (ids, graph_json) = generate_pie_chart(os, title, request.session['username'], request.session['start_date'],
                                       request.session['end_date'])

    return render(request, 'stats/os_stats.html', {'ids': ids, 'graph_json': graph_json})