from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required

import csv
from alexdaphne.models import RsvpReply, Guest, Location, Event, ATTENDANCE_CHOICES



def contact(request):
    return render_to_response('contact.html', {})


def maps(request):
    return render_to_response('maps.html', {})


def photos(request):
    return render_to_response('photos.html', {})


def thankyou(request):
    return render_to_response('thankyou.html', {})


def home(request):
    form = {"name_count" : "0"}
    return render_to_response('home.html', {'form' : form})


def rsvp_add(request):

    def validate(form):
        errors = {}
        ERR_MSG = "This field is required."

        if "name0" not in form:
            errors["name0"] = ERR_MSG
        if len(form["name0"].strip()) == 0:
            errors["name0"] = ERR_MSG

        if "num_reception" not in form:
            errors["num_reception"] = ERR_MSG
        try:
            int(form["num_reception"])
        except ValueError:
            errors["num_reception"] = ERR_MSG

        if "num_ceremony" not in form:
            errors["num_ceremony"] = ERR_MSG
        try:
            int(form["num_ceremony"])
        except ValueError:
            errors["num_ceremony"] = ERR_MSG

        if "name_count" not in form:
            errors["name_count"] = ERR_MSG
        try:
            int(form["name_count"])
        except ValueError:
            errors["name_count"] = ERR_MSG

        if errors:
            errors["message"] = "Oops, something went wrong!"
        return errors


    if not request.POST:
        return HttpResponseRedirect("/")
    else:
        form = request.POST
        errors = validate(form)
        
        if errors:
            class Name:
                def __init__(self, key, val):
                    self.key = key
                    self.val = val
               
            additional_names = []
            names = [k for k in form if k.startswith("name") and k != "name0"]
            
            for name in names:
                try:
                    int(name[4:])
                    additional_names.append( Name(name, form[name]) )
                except ValueError:
                    pass
            
            return render_to_response('home.html',
                    {'form'   : form,
                     'errors' : errors,
                     'additional_names' : additional_names})
        
        else:
            r = RsvpReply(
                    comment      = form["comment"],
                    num_ceremony = int(form["num_ceremony"]),
                    num_reception= int(form["num_reception"])
                    )
            r.save()

            upperbound = int(form["name_count"]) + 1
            for i in range(0, upperbound):
                try:
                    guest_name = form["name%s" % i].strip()
                    if len(guest_name) > 0:
                        g = Guest(name=guest_name)
                        g.rsvp_reply_id = r.id
                        g.save()
                except KeyError:
                    pass

            return HttpResponseRedirect('/thankyou')


@login_required
def rsvp_dump(request):
    filename = 'rsvp.csv'
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=%s' % filename

    writer = csv.writer(response)
    
    # loop through the RsvpReply objects
    rsvplist = RsvpReply.objects.all()
    for rsvp in rsvplist:
        is_first_row = True
        guests = rsvp.guest_set.all()
        for g in guests:
            if is_first_row:
                writer.writerow(
                   [rsvp.id,
                    g.name,
                    rsvp.num_ceremony,
                    rsvp.num_reception,
                    rsvp.taken_care_of,
                    rsvp.received_date,
                    rsvp.comment])
                is_first_row = False
            else:
                writer.writerow(['', g.name, '', '', '', '', ''])
    return response

