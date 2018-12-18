from django import template
from django.templatetags.static import StaticNode
from django.contrib.staticfiles.storage import staticfiles_storage
import os

register = template.Library()


class StaticFilesNode(StaticNode):
    def url(self, context):
        path = self.path.resolve(context)
        i = path.find("?")
        if i == -1:
            file_path, query = path, ""
        else:
            file_path, query = path[:i], path[i + 1:]

        try:
            mtime = int(os.path.getmtime(staticfiles_storage.path(file_path)))
        except OSError:
            try:
                mtime = int(
                    os.path.getmtime(staticfiles_storage.path(file_path).replace("\\static\\", "\\polls\\static\\")))
            except OSError:
                mtime = None

        mtime_query = "v=%s" % (mtime or "")
        if query:
            mtime_query = "&%s" % mtime_query

        result = staticfiles_storage.url(file_path)
        if mtime:
            return "%s?%s%s" % (result, query, mtime_query)
        return result


@register.tag('static')
def do_static(parser, token):
    return StaticFilesNode.handle_token(parser, token)
