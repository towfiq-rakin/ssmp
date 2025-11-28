"""
Analytics Module
Handles all dashboard analytics and chart generation
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64
from extensions import db
from models import User, AcademicRecord, Scholarship, Stipend


def generate_cgpa_distribution_chart(dept_id):
    """Generate CGPA distribution histogram"""
    cgpas = []
    academic_records = db.session.query(AcademicRecord).select_from(User).join(
        AcademicRecord, User.student_id == AcademicRecord.student_id
    ).filter(User.dept_id == dept_id).all()
    
    for record in academic_records:
        if record.cgpa:
            cgpas.append(record.cgpa)
    
    plt.figure(figsize=(10, 6))
    plt.hist(cgpas, bins=15, color='#4caf50', edgecolor='black', alpha=0.7)
    plt.xlabel('CGPA', fontsize=12)
    plt.ylabel('Number of Students', fontsize=12)
    plt.grid(axis='y', alpha=0.3, linestyle='--')
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight', dpi=100)
    img.seek(0)
    plot_data = base64.b64encode(img.getvalue()).decode()
    plt.close()
    
    return plot_data, cgpas


def generate_last_semester_gpa_chart(dept_id):
    """Generate last semester GPA distribution histogram"""
    last_semester_gpas = []
    academic_records = db.session.query(AcademicRecord).select_from(User).join(
        AcademicRecord, User.student_id == AcademicRecord.student_id
    ).filter(User.dept_id == dept_id).all()
    
    for record in academic_records:
        last_gpa = record.get_last_semester_gpa()
        if last_gpa:
            last_semester_gpas.append(last_gpa)
    
    plt.figure(figsize=(10, 6))
    plt.hist(last_semester_gpas, bins=15, color='#2196f3', edgecolor='black', alpha=0.7)
    plt.xlabel('Last Semester GPA', fontsize=12)
    plt.ylabel('Number of Students', fontsize=12)
    plt.grid(axis='y', alpha=0.3, linestyle='--')
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight', dpi=100)
    img.seek(0)
    plot_data = base64.b64encode(img.getvalue()).decode()
    plt.close()
    
    return plot_data, last_semester_gpas


def generate_budget_utilization_chart(dept_id, remaining_budget):
    """Generate budget utilization pie chart"""
    spent_scholarships = db.session.query(db.func.sum(Scholarship.amount)).select_from(User).join(
        Scholarship, User.student_id == Scholarship.student_id
    ).filter(User.dept_id == dept_id).scalar() or 0
    
    spent_stipends = db.session.query(db.func.sum(Stipend.amount)).select_from(User).join(
        Stipend, User.student_id == Stipend.student_id
    ).filter(User.dept_id == dept_id).scalar() or 0
    
    plt.figure(figsize=(10, 6))
    labels = ['Remaining Budget', 'Scholarships Spent', 'Stipends Spent']
    sizes = [remaining_budget, spent_scholarships, spent_stipends]
    colors = ['#e0e0e0', '#4caf50', '#2196f3']
    explode = (0.05, 0, 0)
    
    plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
            shadow=True, startangle=140, textprops={'fontsize': 11})
    
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight', dpi=100)
    img.seek(0)
    plot_data = base64.b64encode(img.getvalue()).decode()
    plt.close()
    
    return plot_data, spent_scholarships, spent_stipends


def generate_awards_breakdown_chart(dept_id):
    """Generate awards breakdown bar chart"""
    scholarship_count = db.session.query(Scholarship).select_from(User).join(
        Scholarship, User.student_id == Scholarship.student_id
    ).filter(User.dept_id == dept_id).count()
    
    stipend_count = db.session.query(Stipend).select_from(User).join(
        Stipend, User.student_id == Stipend.student_id
    ).filter(User.dept_id == dept_id).count()
    
    plt.figure(figsize=(10, 6))
    categories = ['Scholarships', 'Stipends']
    counts = [scholarship_count, stipend_count]
    bars = plt.bar(categories, counts, color=['#4caf50', '#2196f3'], width=0.5)
    
    # Add value labels on top of bars
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}',
                ha='center', va='bottom', fontsize=12, fontweight='bold')
    
    plt.ylabel('Count', fontsize=12)
    plt.xlabel('Award Type', fontsize=12)
    plt.grid(axis='y', alpha=0.3, linestyle='--')
    plt.xticks(fontsize=11)
    plt.yticks(fontsize=10)
    
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight', dpi=100)
    img.seek(0)
    plot_data = base64.b64encode(img.getvalue()).decode()
    plt.close()
    
    return plot_data, scholarship_count, stipend_count


def get_admin_dashboard_data(dept_id, remaining_budget):
    """
    Generate all analytics data for admin dashboard
    
    Args:
        dept_id: Department ID
        remaining_budget: Current remaining budget
        
    Returns:
        dict: Contains stats and plots data
    """
    # Get student count
    total_students = User.query.filter_by(dept_id=dept_id).count()
    
    # Generate charts and get data
    plot_cgpa, cgpas = generate_cgpa_distribution_chart(dept_id)
    plot_last_gpa, last_semester_gpas = generate_last_semester_gpa_chart(dept_id)
    plot_budget, spent_scholarships, spent_stipends = generate_budget_utilization_chart(dept_id, remaining_budget)
    plot_awards, scholarship_count, stipend_count = generate_awards_breakdown_chart(dept_id)
    
    # Calculate statistics
    avg_cgpa = round(sum(cgpas)/len(cgpas), 2) if cgpas else 0
    avg_last_gpa = round(sum(last_semester_gpas)/len(last_semester_gpas), 2) if last_semester_gpas else 0
    total_spent = spent_scholarships + spent_stipends
    
    return {
        'stats': {
            'total_students': total_students,
            'avg_cgpa': avg_cgpa,
            'avg_last_gpa': avg_last_gpa,
            'scholarship_count': scholarship_count,
            'stipend_count': stipend_count,
            'total_spent': total_spent,
            'remaining_budget': remaining_budget
        },
        'plots': {
            'cgpa': plot_cgpa,
            'last_gpa': plot_last_gpa,
            'budget': plot_budget,
            'awards': plot_awards
        }
    }
