from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import ContributionList, MonthlyContribution, MonthlyExpense, EventType, ExpenseType, UsefulLink, BannerImage, EventGallary, GallaryUploadImage
from account.models import TeamMember
from django.contrib.auth.models import User
from datetime import date
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

# Create your views here.

@login_required(login_url="/login/")
def home(request):
  data = {
    'page_name' : 'home',
    'bday' : bday_notification()
  }
  return render(request, "dashboard/home.html", data)


@login_required(login_url="/login/")
def team_member(request):
  team_members = TeamMember.objects.values().filter(status=1)
  emp_data = []
  for member in team_members:
    emp_user_data = User.objects.values().filter(id=member['name_id'])
    emp_dict = {
        'name'       : str(emp_user_data[0]['first_name']) + ' ' + str(emp_user_data[0]['last_name']),
        'emp_id'     : member['emp_id'],
        'email'      : member['email'],
        'contact_no' : member['contact_no'],
        'dob'        : member['dob'],
        'gender'     : member['gender'],
        'about_me'   : member['about_me']
        }
    emp_data.append(emp_dict)
  emp_sorted_data = sorted(emp_data, key = lambda i: i['name'])
  data = {
    'data' : emp_sorted_data,
    'page_name' : 'members',
    'bday' : bday_notification()
  }
  return render(request, "dashboard/team_members.html", data)


@login_required(login_url="/login/")
def team_contri(request):
  today = date.today()
  m = today.month
  y = today.year
  url = '/team/contribution/'+str(m)+'/'+str(y)
  return HttpResponseRedirect(url)


@login_required(login_url="/login/")
def team_contribution(request, m, y):
  if request.method == 'POST':
    user_contri_id = [key for key, value in request.POST.items() if key.isdigit()]
    for ids in user_contri_id:
      update_contri = MonthlyContribution.objects.get(pk=int(ids))
      update_contri.date = date.today()
      update_contri.paid = True
      update_contri.save()

  today = date.today()
  pre_month, pre_year, next_month, next_year, balance, mon_balance = 0,0,0,0,0,0
  pre_link, next_link = "",""
  if today.month == m and today.year == y:
    if m == 1:
      pre_month, pre_year = 12, y-1
    else:
      pre_month, pre_year = m-1, y
    pre_link = 'team/contribution/'+str(pre_month)+'/'+str(pre_year)
  else:
    if m == 1:
      pre_month, pre_year = 12, y-1
      next_month, next_year = m+1, y
    elif m == 12:
      pre_month, pre_year = m-1, y
      next_month, next_year = 1, y+1
    else:
      pre_month, pre_year = m-1, y
      next_month, next_year = m+1, y
    pre_link = 'team/contribution/'+str(pre_month)+'/'+str(pre_year)
    next_link = 'team/contribution/'+str(next_month)+'/'+str(next_year)


  total_collection = MonthlyContribution.objects.values()
  total_income = sum(contri['amount'] for contri in total_collection if contri['paid']==True)
  total_expenses = MonthlyExpense.objects.values()
  total_expense = sum(exp['ExpenseAmount'] for exp in total_expenses)
  total_balance = total_income - total_expense

  monthly_contro_list_id = ContributionList.objects.values().filter(date__month=m, date__year=y)
  if monthly_contro_list_id:
    monthly_contribution = MonthlyContribution.objects.filter(contri_title_id=monthly_contro_list_id[0]['id']).values()
    contri_list = []
    for data in monthly_contribution:
      member_id = TeamMember.objects.only('id').get(id = data['user_id']).id
      user_detail = (User.objects.values().filter(id=member_id))[0]
      result = {
      'name' : str(user_detail['first_name'])+ ' '+ str(user_detail['last_name']),
      'amount' : data['amount'],
      'paid' : data['paid'],
      'contri_id' : data['id']
      }
      contri_list.append(result)
    contri_list = sorted(contri_list, key = lambda i: i['name'])
    monthly_income = sum(contri['amount'] for contri in monthly_contribution if contri['paid']==True)
    is_contri_paid = any(data['user_id'] == request.user.id for data in monthly_contribution if data['paid']==True)
  else:
    contri_list = []
    monthly_income = 0
    is_contri_paid = False

  month_history = []
  for data in ContributionList.objects.values().filter(date__year=y):
    result = MonthlyContribution.objects.filter(contri_title_id=data['id'], user_id = request.user.id).values()
    detail = {
      'date' : data['date'],
      'amount' : result[0]['amount'],
      'paid' : result[0]['paid'],
      'paid_on' : result[0]['date']
    }
    month_history.append(detail)

  mon_expense, exp_list = monthly_expense_data(m,y)
  mon_balance = monthly_income - mon_expense

  data = {
    'income' : total_income,
    'total_expense' : total_expense,
    'balance' : total_balance,
    'mon_expense' : mon_expense,
    'mon_contri' : monthly_income,
    'mon_balance' : mon_balance,
    'date' : date(y, m, 1).strftime("%B %Y"),
    'expense' : exp_list,
    'pre_link' : pre_link,
    'next_link' : next_link,
    'page_name' : 'contribution',
    'monthly_contri_history' : month_history,
    'is_contri_paid':is_contri_paid,
    'monthly_contribution' : contri_list,
    'm' : m,
    'y' : y,
    'bday' : bday_notification()
  }

  return render(request, "dashboard/team_contribution.html", data)


def monthly_expense_data(m, y):
  exp_lst = []
  mon_expense = 0
  expense = MonthlyExpense.objects.values().filter(date__month=m, date__year=y)
  if expense:
    mon_expense = sum(item['ExpenseAmount'] for item in expense)
    for e in expense:
      expense_type = (ExpenseType.objects.filter(id=e['ExpenseCategory_id']).values())[0]['title'] if e['ExpenseCategory_id'] else '--'
      event = (EventType.objects.filter(id=e['EventCategory_id']).values())[0]['title'] if e['EventCategory_id'] else '--'
      whos = (TeamMember.objects.filter(id=e['whos_id']).values())
      if whos:
        user = User.objects.values().filter(id=whos[0]['name_id'])
        user_name = str(user[0]['first_name']) + ' ' + str(user[0]['last_name'])
      else:
        user_name = '- - -'
      exp_dic = {
        'date':e['date'],
        'expense_type':expense_type,
        'event':event,
        'whos':user_name,
        'amount':e['ExpenseAmount']
      }
      exp_lst.append(exp_dic)
  return mon_expense, exp_lst


@login_required(login_url="/login/")
def useful_link(request):
  #If user add the links through frontend web form
  if request.method == 'POST':
    #updating an existing useful link
    if request.POST['link_id']:
      update_link = UsefulLink.objects.get(pk=request.POST['link_id'])
      update_link.title = request.POST['link_title']
      update_link.link = request.POST['link_path']
      update_link.save()
    #Adding new useful link
    else:
      title = request.POST['link_title']
      path =  request.POST['link_path']
      link = UsefulLink(title=title, link=path)
      link.save()

  links_data = UsefulLink.objects.values()

  #Query logic to search links
  search = request.GET.get('search', None)
  if search is not None:
    links_data = links_data.filter(
      Q(title__icontains=search) | Q(link__icontains=search)
      )

  #Paginations if records are more than 25
  page = request.GET.get('page', 1)
  paginator = Paginator(links_data, 20)
  try:
      links = paginator.page(page)
  except PageNotAnInteger:
      links = paginator.page(1)
  except EmptyPage:
      links = paginator.page(paginator.num_pages)

  data = {
    'link' : links,
    'page_name' : 'useful_link',
    'bday' : bday_notification()
  }
  return render(request, "dashboard/useful_links.html", data)


@login_required(login_url="/login/")
def gallery(request, y):
  banner = BannerImage.objects.all().filter(year=y)
  eventimg = EventGallary.objects.values().filter(date__year=y)
  e_id = EventType.objects.only('id').get(title = 'Birthday').id
  f_id = EventType.objects.only('id').get(title = 'Farewell').id
  bdayimg = list(item for item in eventimg if item['event_id']==e_id)
  farewell_img = list(item for item in eventimg if item['event_id']==f_id)
  otherimg = list(item for item in eventimg if item['event_id']!=e_id and item['event_id']!=f_id)
  data = {
    'banner' : banner,
    'bdayimg' : bdayimg,
    'farewell_img' : farewell_img,
    'otherimg' : otherimg,
    'current_y' : y,
    'page_name' : 'gallery',
    'bday' : bday_notification()
  }
  return render(request, "dashboard/gallery.html", data)


@login_required(login_url="/login/")
def gallery_show_imgs(request, y, title, img_id):
  imgs = GallaryUploadImage.objects.all().filter(title_id = img_id)
  data = {
    'title':title,
    'y':y,
    'imgs' : imgs,
    'page_name' : 'gallery',
    'bday' : bday_notification()
  }
  return render(request, "dashboard/gallery_images.html", data)


def bday_notification():
  today = date.today()
  team_dob = TeamMember.objects.values().filter(dob__month=today.month).order_by('dob');
  bday_lst = []
  for dob in team_dob:
    if dob['dob'].day == today.day :
      birthday_user = (User.objects.values().filter(id=dob['name_id']))[0]
      bday_lst.append('Today is '+str(birthday_user['first_name'])+ ' '+
        str(birthday_user['last_name'])+"'s birthday.")
    if dob['dob'].day > today.day :
      birthday_user = (User.objects.values().filter(id=dob['name_id']))[0]
      bday_lst.append(str(birthday_user['first_name'])+ ' '+
        str(birthday_user['last_name'])+ ' - ' + str(dob['dob'].strftime("%d, %B")))
  return bday_lst
