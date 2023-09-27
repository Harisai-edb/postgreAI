from django.shortcuts import render
from .models import Employee,Fuelconsumption,WeatherData,Sales
from django.db.models import Count
import matplotlib.pyplot as plt
import pandas as pd
import os
from django.apps import apps
from io import StringIO
from django.urls import reverse


def home(request):
    context = {
        'project_title': 'PostgreAI',
        'subtitle': 'Intelligence to Postgres',
        'data_analysis_description': 'Data Analysis description goes here.',
        'forecasting_description': 'Forecasting description goes here.',
    }
    return render(request, 'pgai/home.html', context)


def model_list(request):
    # Get a list of all your Django models
    app_name = 'empstat'
    models = apps.get_app_config(app_name).get_models() 
    # app = apps.get_app_config(app_name)
    # models = app.get_models()

    # Create a list of dictionaries with model names and their URLs
    model_data = []
    for model in models:
        model_data.append({
            'model_name': model._meta.verbose_name,
            'model_url':  reverse('model_details', args=[model._meta.object_name])
        })
    
    # Pass the list of model names to the template
    context = {
        'models': model_data,
    }

    return render(request, 'pgai/model_list.html', context)

def model_details(request, model_name):
    # Find the model based on the name in the URL
    model = apps.get_model('empstat', model_name)

    # Retrieve data from the selected model and convert it to a DataFrame
    queryset = model.objects.all().values()
    df = pd.DataFrame.from_records(queryset)

    # Calculate summary statistics (describe)
    describe_data = df.describe()

    # Capture the output of df.info() as a string
    info_output = StringIO()
    df.info(buf=info_output)
    info_data = info_output.getvalue()
    info_output.close()

    # Pass the model details to the template
    context = {
        'model_name': model_name,
        'data_frame': df.head().to_html(classes='table table-striped table-bordered table-sm'),
        'describe': describe_data.to_html(classes='table table-striped table-bordered table-sm'),
        'info': info_data,
    }

    return render(request, 'pgai/model_details.html', context)




def data_analysis_model(request, model_name):
    model = apps.get_model('empstat', model_name)
    data = model.objects.all()
    analysis_results = analyze_discreate_data_model(data)
    context = {
        'analysis_result': analysis_results,
    }
    return render(request, 'pgai/data_analysis.html', context)


def analyze_discreate_data_model(data):
    if not data:
        return "No data to analyze."

    columns_info = []
    for field in data[0]._meta.get_fields():
        column_name = field.name
        column_type = field.get_internal_type()

        # Check if the column contains discrete strings or numbers
        is_discrete_string = False
        is_discrete_to_show = False
        is_number = False
        distinct_values = list()
        count_of_col = len(data)
        chart_filename = 'image.png'


        if column_type == 'CharField' or column_type == 'TextField':
            is_discrete_string = True
            distinct_values = data.values_list(column_name, flat=True).distinct()
            if len(distinct_values) <= 0.4 * count_of_col:
                is_discrete_to_show = True
                        # Generate a bar chart for discrete columns
                if distinct_values:
                    plt.figure(figsize=(15, 6))
                    plt.bar(distinct_values, [data.filter(**{column_name: val}).count() for val in distinct_values])
                    plt.title(f'Distinct Values Count for {column_name}')
                    plt.xlabel(column_name)
                    plt.ylabel('Count')
                    plt.xticks(rotation=45)
                    plt.tight_layout()
                    chart_filename = f'{column_name}_chart.png'
                    plt.savefig(os.path.join('empstat/static/pgai/', chart_filename))
                    plt.close()
        elif column_type in ['IntegerField', 'FloatField', 'DecimalField']:
                is_number = True
                

        columns_info.append({
            'column_name': column_name,
            'column_type': column_type,
            'is_discrete_string': is_discrete_string,
            'is_number': is_number,
            'distinct_values': distinct_values,
            'count_of_col': count_of_col,
            'is_discrete_to_show': is_discrete_to_show,
            'chart_filename': chart_filename,

        })

    return columns_info


#  Old code

def ml_features(request):
    app_name = 'empstat'
    models = apps.get_app_config(app_name).get_models()
    model_data = {}
    # records_count = WeatherData.objects.count()

    # Distinct departments and their counts
    # station_city = WeatherData.objects.values('Station_City').annotate(count=Count('Station_City'))

    for model in models:
        # Retrieve data from the current model and convert it to a DataFrame
        queryset = model.objects.all().values()
        df = pd.DataFrame.from_records(queryset)

        # Calculate summary statistics (describe)
        describe_data = df.describe()

        # Capture the output of df.info() as a string
        info_output = StringIO()
        df.info(buf=info_output)
        info_data = info_output.getvalue()
        info_output.close()

        # Store the data for the current model in the dictionary
        model_name = model.__name__
        model_data[model_name] = {
            'data_frame': df.head().to_html(classes='table table-striped table-bordered table-sm'),
            'describe': describe_data.to_html(classes='table table-striped table-bordered table-sm'),
            'info': info_data,
        }

    # Pass the model data to the template
    context = {
        'model_data': model_data,
    }

    return render(request, 'pgai/ml_features.html', context)



def data_analysis(request):
    data = Fuelconsumption.objects.all()
    analysis_results = analyze_discreate_data(data)
    context = {
        'analysis_result': analysis_results,
    }
    return render(request, 'pgai/data_analysis.html', context)


def analyze_discreate_data(data):
    if not data:
        return "No data to analyze."

    columns_info = []
    for field in data[0]._meta.get_fields():
        column_name = field.name
        column_type = field.get_internal_type()

        # Check if the column contains discrete strings or numbers
        is_discrete_string = False
        is_discrete_to_show = False
        is_number = False
        distinct_values = list()
        count_of_col = len(data)
        chart_filename = 'image.png'


        if column_type == 'CharField' or column_type == 'TextField':
            is_discrete_string = True
            distinct_values = data.values_list(column_name, flat=True).distinct()
            if len(distinct_values) <= 0.4 * count_of_col:
                is_discrete_to_show = True
                        # Generate a bar chart for discrete columns
                if distinct_values:
                    plt.figure(figsize=(15, 6))
                    plt.bar(distinct_values, [data.filter(**{column_name: val}).count() for val in distinct_values])
                    plt.title(f'Distinct Values Count for {column_name}')
                    plt.xlabel(column_name)
                    plt.ylabel('Count')
                    plt.xticks(rotation=45)
                    plt.tight_layout()
                    chart_filename = f'{column_name}_chart.png'
                    plt.savefig(os.path.join('empstat/static/pgai/', chart_filename))
                    plt.close()
        elif column_type in ['IntegerField', 'FloatField', 'DecimalField']:
                is_number = True
                

        columns_info.append({
            'column_name': column_name,
            'column_type': column_type,
            'is_discrete_string': is_discrete_string,
            'is_number': is_number,
            'distinct_values': distinct_values,
            'count_of_col': count_of_col,
            'is_discrete_to_show': is_discrete_to_show,
            'chart_filename': chart_filename,

        })

    return columns_info

def timeseries_analysis(request):
    data = WeatherData.objects.all()
    analysis_results = analyze_timeseries_data(data)
    context = {
        'analysis_result': analysis_results,
    }
    return render(request, 'pgai/data_analysis.html', context)

def analyze_timeseries_data(data):
    if not data:
        return "No data to analyze."
    
    columns_info = []
    for field in data[0]._meta.get_fields():
        column_name = field.name
        column_type = field.get_internal_type()

        # Check if the column contains discrete strings or numbers
        is_discrete_string = False
        is_discrete_to_show = False
        is_number = False
        distinct_values = list()
        count_of_col = len(data)
        chart_filename = 'image.png'
        timestamp_column = ''

        if column_type == 'CharField' or column_type == 'TextField':
            is_discrete_string = True
            distinct_values = data.values_list(column_name, flat=True).distinct()
            # if len(distinct_values) <= 0.1 * count_of_col and len(distinct_values) <= 55:
            if  len(distinct_values) <= 55:
                is_discrete_to_show = True
                        # Generate a bar chart for discrete columns
                if distinct_values:
                    plt.figure(figsize=(25, 6))
                    plt.bar(distinct_values, [data.filter(**{column_name: val}).count() for val in distinct_values])
                    plt.title(f'Distinct Values Count for {column_name}')
                    plt.xlabel(column_name)
                    plt.ylabel('Count')
                    plt.xticks(rotation=45)
                    plt.tight_layout()
                    chart_filename = f'{column_name}_chart.png'
                    plt.savefig(os.path.join('empstat/static/pgai/', chart_filename))
                    plt.close()
        elif column_type in ['IntegerField', 'FloatField', 'DecimalField']:
                is_number = True
                timestamp_column = 'Date_Full'  # Replace with your timestamp column name

                new_york_data = data.filter(Station_City="New York")

                # Generate a line chart for numeric columns based on timestamp
                if timestamp_column:
                    df = pd.DataFrame(list(new_york_data.values(timestamp_column, column_name)))
                    df.set_index(timestamp_column, inplace=True)
                    plt.figure(figsize=(20, 6))
                    plt.scatter(df.index, df[column_name])
                    plt.title(f'{column_name} Over Time')
                    plt.xlabel(timestamp_column)
                    plt.ylabel(column_name)
                    plt.xticks(rotation=45)
                    plt.tight_layout()
                    chart_filename = f'{column_name}_vs_date_chart.png'
                    plt.savefig(os.path.join('empstat/static/pgai', chart_filename))
                    plt.close()

    
        columns_info.append({
            'column_name': column_name,
            'column_type': column_type,
            'is_discrete_string': is_discrete_string,
            'is_number': is_number,
            'distinct_values': distinct_values,
            'count_of_col': count_of_col,
            'is_discrete_to_show': is_discrete_to_show,
            'chart_filename': chart_filename,
            'timestamp_column': timestamp_column,

        })

    return columns_info


def sales_analysis(request):
    data = Sales.objects.all()
    analysis_results = analyze_sales_data(data)
    context = {
        'analysis_result': analysis_results,
    }
    return render(request, 'pgai/sales_analysis.html', context)

def analyze_sales_data(data):
    if not data:
        return "No data to analyze."
    
    columns_info = []
    for field in data[0]._meta.get_fields():
        column_name = field.name
        column_type = field.get_internal_type()

        # Check if the column contains discrete strings or numbers
        is_discrete_string = False
        is_discrete_to_show = False
        is_number = False
        distinct_values = list()
        count_of_col = len(data)
        chart_filename = 'image.png'
        timestamp_column = ''
        year = 0

        if column_type == 'CharField' or column_type == 'TextField':
            is_discrete_string = True
            distinct_values = data.values_list(column_name, flat=True).distinct()
            # if len(distinct_values) <= 0.1 * count_of_col and len(distinct_values) <= 55:
            if  len(distinct_values) <= 0.5 * count_of_col:
                is_discrete_to_show = True
                # Generate a bar chart for discrete columns
                if distinct_values:
                    plt.figure(figsize=(25, 6))
                    plt.bar(distinct_values, [data.filter(**{column_name: val}).count() for val in distinct_values])
                    plt.title(f'Distinct Values Count for {column_name}')
                    plt.xlabel(column_name)
                    plt.ylabel('Count')
                    plt.xticks(rotation=45)
                    plt.tight_layout()
                    chart_filename = f'{column_name}_sales_chart.png'
                    plt.savefig(os.path.join('empstat/static/pgai/', chart_filename))
                    plt.close()

                    columns_info.append({
                    'column_name': column_name,
                    'column_type': column_type,
                    'is_discrete_string': is_discrete_string,
                    'is_number': is_number,
                    'distinct_values': distinct_values,
                    'count_of_col': count_of_col,
                    'is_discrete_to_show': is_discrete_to_show,
                    'chart_filename': chart_filename,
                    'timestamp_column': timestamp_column,
                    

                     })

            


        elif column_type in ['IntegerField', 'FloatField', 'DecimalField']:
                is_number = True
                timestamp_column = 'orderdate'  # Replace with your timestamp column name

                # new_york_data = data.filter(Station_City="New York")
                
                unique_years = data.values_list('year_id', flat=True).distinct()
                if timestamp_column:
                # Generate a line chart for numeric columns based on timestamp
                    for year in sorted(unique_years):
                        year_data = data.filter(year_id=year)
                        df = pd.DataFrame(list(year_data.values(timestamp_column, column_name)))
                        df.set_index(timestamp_column, inplace=True)
                        plt.figure(figsize=(50, 6))
                        plt.scatter(df.index, df[column_name])
                        plt.title(f'{column_name} Over Time')
                        plt.xlabel(timestamp_column)
                        plt.ylabel(column_name)
                        plt.xticks(rotation=45)
                        plt.tight_layout()
                        chart_filename = f'{column_name}_vs_date_for_{year}_chart.png'
                        plt.savefig(os.path.join('empstat/static/pgai', chart_filename))
                        plt.close()

                        columns_info.append({
                        'column_name': column_name,
                        'column_type': column_type,
                        'is_discrete_string': is_discrete_string,
                        'is_number': is_number,
                        'distinct_values': distinct_values,
                        'count_of_col': count_of_col,
                        'is_discrete_to_show': is_discrete_to_show,
                        'chart_filename': chart_filename,
                        'timestamp_column': timestamp_column,
                        'year': year,

                         })



    
        

    return columns_info

