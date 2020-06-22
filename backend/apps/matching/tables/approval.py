import django_tables2 as tables
from django_tables2 import TemplateColumn

from apps.matching.models import Participant
from apps.matching.src.dual_factory import instanciate_for_participants

approval_button = '<form>{% csrf_token %}<input type="hidden" value="{{record.uuid}}" name="uuid"> <button type="submit" name="change_approval" formmethod="post" class="btn btn-sm {% if record.is_approved %} btn-warning {% else %} btn-success {%endif%}">{% if record.is_approved %}Disapprove{% else %}  Approve {%endif%}</button></form>'
info_button = (
    '<a class="btn btn-info btn-sm" href="/matching/hospital_view/{{record.uuid }}">More Info </a>'
)
delete_button = (
    "<!-- Button trigger modal -->"
    '<button type="button" class="btn btn-sm btn-danger" data-toggle="modal" data-target="#exampleModal{{record.uuid}}">'
    "Delete"
    "</button>"
    "<!-- Modal -->"
    '<div class="modal fade" id="exampleModal{{record.uuid}}" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">'
    '  <div class="modal-dialog" role="document">'
    '    <div class="modal-content">'
    '      <div class="modal-header">'
    '        <h5 class="modal-title" id="exampleModalLabel">Are you sure?</h5>'
    '        <button type="button" class="close" data-dismiss="modal" aria-label="Close">'
    '          <span aria-hidden="true">&times;</span>'
    "        </button>"
    "      </div>"
    '      <div class="modal-body">'
    "        Are you sure you want to delete the user with email {{record.user}}?"
    "      </div>"
    '      <div class="modal-footer">'
    '        <button type="button" class="btn btn-secondary" data-dismiss="modal">Cancel</button>'
    '        <form>{% csrf_token %}<input type="hidden" value="{{record.uuid}}" name="uuid"><button  type="submit" name="delete"  class="btn btn-danger" formmethod="post">Yes, delete.</button></form>'
    "      </div>"
    "    </div>"
    "  </div>"
    "</div>"
)


def make_staff_approvals_table(p_type):
    class ApproveParticipantTable(tables.Table):
        info = TemplateColumn(template_code=info_button)
        status = TemplateColumn(template_code=approval_button)
        delete = TemplateColumn(template_code=delete_button)

        class Meta:
            model = Participant[p_type]
            template_name = "django_tables2/bootstrap4.html"
            fields = ["user__email"]

    return ApproveParticipantTable


ApproveParticipantTable = instanciate_for_participants(make_staff_approvals_table)
