from django.db import models


ATTENDANCE_CHOICES = (
        (0, "Sorry, can't attend"),
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'),
)


class RsvpReply(models.Model):
    comment = models.TextField(
            "Hmm... any other comments?", maxlength=500, null=True, blank=True)
    
    num_ceremony = models.IntegerField("Church & Lunch",
            choices=ATTENDANCE_CHOICES,
            help_text="Number of people that will attend the church ceremony.")
    
    num_reception = models.IntegerField("Dinner Reception",
            choices=ATTENDANCE_CHOICES,
            help_text="Number of people that will attend the reception dinner.")
    
    received_date = models.DateTimeField("Received On",
            auto_now_add=True)

    taken_care_of = models.BooleanField("Taken Care Of?",
            help_text="Checkmark it if you have taken care of this RSVP already.")

    def __str__(self):
        guests = Guest.objects.filter(rsvp_reply=self)
        if len(guests) > 1:
            return ", ".join([g.name for g in guests])
        else:
            return guests[0].name

    class Admin:
        list_display = ('__str__', 'num_ceremony', 'num_reception',
                'taken_care_of', 'received_date')
        ordering = ['-received_date', '__str__']
        fields = (
                (None, {
                    'fields': ('received_date', 'taken_care_of',
                        'num_ceremony', 'num_reception', 'comment')
                    }
                ),
        )


class Guest(models.Model):
    name = models.CharField(maxlength=80, core=True)
    rsvp_reply = models.ForeignKey(RsvpReply, edit_inline=models.TABULAR,
            num_in_admin=2, num_extra_on_change=2)

    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField("Location", maxlength=30)
    description = models.TextField(maxlength=30, null=True, blank=True)
    address = models.TextField("Where", maxlength=100)
    geocode_latitude = models.FloatField(max_digits=9, decimal_places=6)
    geocode_longitude = models.FloatField(max_digits=9, decimal_places=6)
    
    def __str__(self):
        return self.name

    class Admin:
        pass


class Event(models.Model):
    name = models.CharField("Event", maxlength=30, core=True)
    event_date = models.DateTimeField("When", null=True)
    description = models.TextField(maxlength=300, blank=True, null=True)
    locations = models.ManyToManyField(Location, null=True,
            filter_interface=models.HORIZONTAL)

    def __str__(self):
        return self.name

    class Admin:
        list_display = ('name', 'event_date')
        ordering = ['-event_date']
        date_hierarchy = 'event_date'

    class Meta:
        get_latest_by = "event_date"
        ordering = ['-event_date']


