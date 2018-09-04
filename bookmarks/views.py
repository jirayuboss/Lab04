from django.shortcuts import render_to_response
from django.template import RequestContext
from bookmarks.forms import SearchForm
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist


def search_page(request):
    form = SearchForm()
    bookmarks = []
    show_results = False
    if 'query' in request.GET:
        show_results = True
        query = request.GET['query'].strip()
        if query:
            form = SearchForm({'query': query})
            bookmarks = bookmarks.objects.filter(
                title_icontains=query
            )[:10]
    variables = RequestContext(request, {
        'form': form,
        'bookmarks': bookmarks,
        'show_results': show_results,
        'show_tags': True,
        'show_user': True
    })
    if request.GET.has_key('AJAX'):
        return render_to_response('bookmark_list.html', variables)
    else:
        return render_to_response('search.html', variables)


def _bookmark_save(request, form):
    # Create or get link.
    link, dummy = \
        Link.objects.get_or_create(url=form.clean_data['url'])
    # Create or get bookmark.
    bookmark, created = Bookmark.objects.get_or_create(
        user=request.user,
        link=link
    )
    # Update bookmark title.
    bookmark.title = form.clean_data['title']
    # If the bookmark is being updated, clear old tag list.
    if not created:
        bookmark.tag_set.clear()
        # Create new tag list.
    tag_names = form.clean_data['tags'].split()
    for tag_name in tag_names:
        tag, dummy = Tag.objects.get_or_create(name=tag_name)
        bookmark.tag_set.add(tag)
        # Save bookmark to database and return it.
        bookmark.save()
        return bookmark


def bookmark_save_page(request):
    if request.method == 'POST' and request.user.is_authenticated():
        form = BookmarkSaveForm(request.POST)
        if form.is_valid():
            bookmark = _bookmark_save(request, form)
            return HttpResponseRedirect(
                '/user/%s/' % request.user.username
            )
        elif request.GET.has_key('url'):
            url = request.GET['url']
            title = ''
            tags = ''
            try:
                link = Link.objects.get(url=url)
                bookmark = Bookmark.objects.get(
                    link=link,
                    user=request.user
                )

            title = bookmark.title
            tags = ' '.join(
                tag.name for tag in bookmark.tag_set.all()
            )
            except ObjectDoesNotExist:
            pass
            form = BookmarkSaveForm({
            'url': url,
            'title': title,
            'tags': tags})
        else:
            form = BookmarkSaveForm()
            variables = RequestContext(request, {
            'form': form
        })
    return render_to_response('bookmark_save.html',
                              variables)
