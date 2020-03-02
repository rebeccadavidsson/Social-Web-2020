#!/usr/bin/python
import os
from django.shortcuts import redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponse
from subprocess import call

# from django.contrib.auth.decorators import permission_required
from .models import Profile, ScheduleItem, Rating
from .scrape import scrape_item
from .helpers import convertdate, refreshschedule


def index(request):
    """ Render main page when website is opened for the first time. """

    # Check if user is logged in
    if not request.user.is_authenticated or request.user.username == "admin":
        return render(request, "login.html")

    # Get user profile and the people this user is following
    profile = Profile.objects.get(user=request.user)
    followers = profile.following.all()

    # Get events from other followers
    empt = []
    for follower in followers:
        to_follow = Profile.objects.get(user__username=follower.username)
        item = ScheduleItem.objects.filter(participants=to_follow).all()
        if item:
            empt.append(item)

    # Index into query if the people you follow also have events
    if empt:
        empt = empt[0]

    events_user = ScheduleItem.objects.filter(participants=profile).all()

    ratings_user = Rating.objects.all()

    rated_events = Rating.objects.filter(user=request.user)


    # user_ratings = []
    # for ratings in events_user:
    #     user_ratings.append(Rating.objects.filter(event=ratings))
    #
    # if user_ratings:
    #     user_ratings = user_ratings[0]


    # Filter events for user
    context = {
        "events": ScheduleItem.objects.all(),
        "events_user": events_user,
        "event_followers": empt,
        "ratings_user": ratings_user,
        "rated_events": rated_events,
        "checker": False
    }

    return render(request, 'mainpage.html', context)


def login_view(request):

    message = None

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # If user already exists, redirect to index
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            message = "Invalid credentials."

        # TODO: Dit afmaken met registeren, model voor User aanmaken
        # return redirect("index")
    return render(request, "login.html", {"message": message})


def register_view(request):
    """Register new user"""

    if request.POST:
        username = request.POST.get('username')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        password = request.POST.get('password')
        password_check = request.POST.get('password_confirm')

        # TODO: dit is veel mooier met JavaScript
        if not username or not password or not password_check:
            return render(request, "register.html", {"message": "Please fill in all fields."})

        # Check if user already exists
        if User.objects.filter(username=username).exists():
            return render(request, "register.html", {"message": "This username is already taken."})

        # Create new user
        user = User.objects.create_user(
            username=username, password=password)
        user.username = username
        user.first_name = firstname
        user.last_name = lastname
        user.save()
        user = authenticate(request, username=username, password=password)

        # Create a new profile! :)
        new_user = Profile(user=user)
        new_user.save()

        if user is not None:
            login(request, user)
            return redirect("index")

    return render(request, "register.html")


def personal_view(request):
    """Render personal profile"""

    # get following user profiles
    profile = Profile.objects.get(user=request.user)
    following = profile.following.all()

    # list with usernames to exclude from 'to_follow', starts with own account
    to_exclude = [request.user.username]

    # get usernames of following users and append to list
    usernames = [person['username'] for person in following.values('username')]
    to_exclude += usernames

    # get all users
    all_users = User.objects.all()

    # show only users that you can follow
    to_follow = User.objects.exclude(username__in=to_exclude)

    # get all events from this user
    events_user = ScheduleItem.objects.filter(participants=profile).all()

    # get all rating from this user
    ratings = Rating.objects.filter(user=request.user).all()

    context = {
        "username": request.user,
        "firstname": request.user.first_name,
        "lastname": request.user.last_name,
        "users": to_follow,
        "following": following,
        "events_user": events_user,
        "ratings": ratings,
        "n": [1,2,3,4,5]
    }
    # TODO
    return render(request, 'personal.html', context)


def searchprofile(request, user):  # TODO, dit moet user_id worden
    """Go to someone else their profile page"""
    # TODO: deze functie en personal_view samenvoegen?
    context = {
        "username": request.user,
        "firstname": request.user.first_name,
        "lastname": request.user.last_name,
        "users": User.objects.all()
    }

    return render(request, 'personal.html', context)


def follow(request, username):
    """Add follower to the profile of logged in user"""

    # get user profiles
    profile = Profile.objects.get(user=request.user)
    to_follow = Profile.objects.get(user__username=username)

    # TODO: if already following user, render message (in context? js?)

    # get user and add to following
    user_to_follow = User.objects.get(username=username)
    profile.following.add(user_to_follow)
    profile.save()

    return redirect("profile")


def unfollow(request, username):
    """Unfollow certain user"""

    # oke dit kan ook in follow functie maar lui en weet niet of dit perse handiger is!!
    profile = Profile.objects.get(user=request.user)
    to_unfollow = Profile.objects.get(user__username=username)
    profile.following.remove(to_unfollow.user)
    profile.save()

    return redirect("profile")


def settings_view(request):
    # TODO
    return redirect("profile")


def schedule_view(request):

    # Check if schedule was already refreshed this day TODO
    # refreshschedule()

    context = {}
    return render(request, 'schedule.html', context)


def addschedule(request):
    """
    Create schedule item.
    default location = universum (TODO!)
    """

    data = scrape_item(request.POST.get("data"))

    # Get user to add to participants
    profile = Profile.objects.get(user=request.user)

    # Check if this item already exists before creating a new one
    # TODO: Sam kan dit mooier? ;)
    try:
        check = ScheduleItem.objects.filter(teacher=data["teacher"],
                                            name=data["sort"],
                                            start=data["start"],
                                            end=data["end"]).first()
    except:
        check = None

    # Add profile to already existing item, else create new item
    if check:
        check.participants.add(profile)
    else:
        # Create new item
        item = ScheduleItem(teacher=data["teacher"],
                            name=data["sort"],
                            start=data["start"],
                            end=data["end"],
                            date=convertdate(data["start"]))
        item.save()
        item.participants.add(profile)

    # TODO wat moet hier?
    return HttpResponse("test")


def review(request, event_id):
    """Save user's review of a training session."""

    # TODO check if comment and rating is entered --> javascript :)
    review = request.POST["comment"]
    rating = request.POST["rating"]

    print(review, rating, event_id, "HSHKFJHSKJ")
    event = ScheduleItem.objects.get(id=event_id)
    # Rating.objects.all().delete()

    # check if user already left rating, ask if they want to rerate the class
    # if Rating.objects.filter(user=request.user, event=event).exists():
    #     return render(request, "/", {"message": "You already left a rating for this course."})

    # create new rating
    new_rating = Rating(user=request.user,
                        comment=review,
                        rating=int(rating),
                        event=event)
    new_rating.save()

    return redirect("/")


def home_view(request):
    context = {}
    # TODO
    return render(request, 'home.html', context)


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        return render(request, "login.html", {"message": "Logged out."})
    else:
        return render(request, "login.html", {"message": "You are already logged out."})



from django import template

register = template.Library()


@register.filter('break')
def break_(loop):
    '''Breaks from a loop.

    The 'break' filter is used within a loop and takes as input a loop variable,
    e.g. 'forloop' in case of a for loop. For example, to display the items
    from list ``items`` up to the first item that is equal to ``end``::

        <ul>
        {% for item in items %}
            {% if item == 'end' %}
                {{ forloop|break }}
            {% endif %}
            <li>{{ item }}</li>
        {% endfor %}
        </ul>

    Breaking from nested loops is also supported by passing the appropriate loop
    variable, e.g. ``forloop.parentloop|break``.
    '''
    raise StopLoopException(loop, False)


@register.filter('continue')
def continue_(loop):
    '''Continues a loop by jumping to its beginning.

    The 'continue' filter is used within a loop and takes as input a loop
    variable, e.g. 'forloop' in case of a for loop. It can also be used (and is
    mostly useful) for nested loops by passing the appropriate loop variable,
    e.g. ``forloop.parentloop|continue``. For example::

        {% for key,values in mapping.iteritems %}<br/>
            {% for value in values %}
                {{ key }}: {{ value }}<br/>
                {% if value|divisibleby:3  %}
                    {{ value }} is divisible by 3<br/>
                    {{ forloop.parentloop|continue }}
                {% endif %}
            {% endfor %}
            {{ key }}: No value divisible by 3<br/>
        {% endfor %}
    '''
    raise StopLoopException(loop, True)
    

class StopLoopException(Exception):
    def __init__(self, loop, continue_, nodelist=None):
        if not isinstance(loop, Loop):
            raise TypeError('Loop instance expected, %s given' % loop.__class__.__name__)
        super(StopLoopException, self).__init__(loop, continue_, nodelist)
        self.loop, self.continue_, self.nodelist = self.args


class Loop(dict):
    '''Base class of loop variables passed in the context (e.g. 'forloop').

    A loop instance holds and keeps up to date the attributes exposed in the
    context. This class exposes ``counter``, ``counter0``, ``first`` and
    ``parentloop``; its :class:`BoundedLoop` subclass adds ``revcounter``,
    ``revcounter0`` and ``last``.

    Additionally, a loop instance renders the items of the nodelist that comprise
    the loop and accumulates the rendered strings on every call to :meth:`next`.
    :meth:`next` also handles continuing or breaking from the loop and informs
    the caller accordingly.
    '''

    PASS = object()
    BREAK = object()
    CONTINUE = object()

    def __init__(self, name, context, nodelist):
        self._name = name
        self._context = context
        self._nodelist = nodelist
        self._rendered_nodelist = template.NodeList()
        self['parentloop'] = context.get(name)
        context.push()
        context[name] = self

    def render(self, close=False):
        '''Renders the accumulated nodelist for this loop.

        As a convenience, if ``close`` is true, the loop is also :meth:`close`d.
        '''
        if close:
            self.close()
        return self._rendered_nodelist.render(self._context)
    render.alters_data = True

    def next(self):
        '''Updates this loop for one iteration step.

        :returns: The status of the loop after this step: :attr:`CONTINUE` if a
            ``continue`` targeting this loop was encountered, :attr:`BREAK` for
            a break, or :attr:`PASS` otherwise.
        :raises StopLoopException: If a ``break`` or ``continue`` for a loop
            other than this one (presumably an ancestor) was encountered.
        '''
        if self._nodelist is None:
            raise RuntimeError('This loop is inactive')
        try: # update the exposed attributes
            counter = self['counter']
            self.update(counter0=counter, counter=counter+1, first=False)
        except KeyError:
            # initialize the exposed attributes the first time this is called
            self.update(counter0=0, counter=1, first=True)
        try:
            _render_nodelist_items(self._nodelist, self._context, self._rendered_nodelist)
            status = self.PASS
        except StopLoopException:
            # if this is not the target loop, keep bubbling up the exception
            if ex.loop is not self:
                raise
            # pop context until (but excluding) the dict that contains this loop
            self._pop_context_until_self(inclusive=False)
            status = ex.continue_ and self.CONTINUE or self.BREAK
        return status
    next.alters_data = True

    def close(self):
        '''Mark this loop as closed.

        After a loop is closed, subsequent calls to :meth:`next` are not allowed.
        This should be called when the loop is "done" to remove any loop-specific
        context entries.
        '''
        if self._nodelist:
            self._pop_context_until_self(inclusive=True)
            self._nodelist = None
    close.alters_data = True

    def _pop_context_until_self(self, inclusive):
        name = self._name
        dicts = self._context.dicts
        while len(dicts) > 1:
            if dicts[-1].get(name) is self:
                if inclusive:
                    del dicts[-1]
                break
            del dicts[-1]


class BoundedLoop(Loop):
    '''A :class:`Loop` of known length.

    ``BoundedLoop`` instances expose ``revcounter``, ``revcounter0`` and ``last``,
    in addition to the attributes exposed by ``Loop`` itself.
    '''

    def __init__(self, name, context, nodelist, length):
        if length < 1:
            raise ValueError('Length must be at least 1')
        self._length = length
        super(BoundedLoop, self).__init__(name, context, nodelist)

    def next(self):
        try: # update the exposed attributes
            revcounter0 = self['revcounter0']
            if revcounter0 <= 0:
                raise RuntimeError('Attempted to call `next()` more than %d times' % self._length)
            self.update(revcounter0=revcounter0-1, revcounter=revcounter0, last=revcounter0==1)
        except KeyError:
            # initialize the exposed attributes the first time this is called
            length = self._length
            self.update(revcounter0=length-1, revcounter=length, last=length==1)
        return super(BoundedLoop, self).next()
    next.alters_data = True


def _render_nodelist_items(nodelist, context, result=None):
    if result is None:
        result = []
    for node in nodelist:
        if not isinstance(node, template.Node):
            result.append(node)
        else:
            try:
                result.append(nodelist.render_node(node, context))
            except Exception:
                # get the wrapped exception if settings.DEBUG is True
                if hasattr(ex, 'exc_info'):
                    ex = ex.exc_info[1]
                # let every exception other than StopLoopException propagate
                if not isinstance(ex, StopLoopException):
                    raise
                # reraise the StopLoopException with the updated nodelist
                if ex.nodelist:
                    result.extend(ex.nodelist)
                ex.nodelist = result
                raise ex
    return result
