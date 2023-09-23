from django.shortcuts import render
from .models import Employee,Fuelconsumption
from django.db.models import Count
import matplotlib.pyplot as plt
import pandas as pd
import os


def ml_features(request):
    # Count of employees
    employee_count = Employee.objects.count()

    # Distinct departments and their counts
    departments = Employee.objects.values('department').annotate(count=Count('department'))

    context = {
        'employee_count': employee_count,
        'departments': departments,
    }
    return render(request, 'pgai/ml_features.html', context)

def data_analysis(request):
    data = Fuelconsumption.objects.all()
    analysis_results = analyze_data(data)
    context = {
        'analysis_result': analysis_results,
    }
    return render(request, 'pgai/data_analysis.html', context)


def analyze_data(data):
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
        count_of_col = Fuelconsumption.objects.count()
        chart_filename = 'image.png'


        if column_type == 'CharField' or column_type == 'TextField':
            is_discrete_string = True
            distinct_values = data.values_list(column_name, flat=True).distinct()
            if len(distinct_values) <= 0.8 * count_of_col:
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
