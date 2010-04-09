# -*- coding: utf-8 -*-
<table class="layout-grid">
<thead>
<tr class="ui-widget-header"><form id="filters" method="get">
    <th class="actions"><span class="ui-icon ui-icon-info"></span></th>
    %for field in collection.render_fields.itervalues():
    <th>
    ${F_(field.label_text or collection.prettify(field.key))|h}
    <a href="${url.current(sortname=field.name, sortorder='asc')}" title="A-Z"><span class="ui-icon ui-icon-circle-arrow-n" style="float: right;"></span></a>
## compose field filter
<%!
from formalchemy import helpers, fatypes
%>
<%
value = request.GET.get(field.name, '')
html = ''
if field.is_relation:
    dummy = field.render()
    options = field.render_opts.get('options', [])
    if len(options) > 0 and options[0] == field._null_option:
        options = options[1:]
    options = [(u'('+F_('All')+')', u'')] + options
    html = helpers.select(field.name, value, options, onchange='reloadPage()')
elif isinstance(field.type, fatypes.Boolean):
    options = [
        (u'('+F_('All')+')', u''),
        (u'('+F_('True')+')', u'0'),
        (u'('+F_('False')+')', u'1'),
    ]
    html = helpers.select(field.name, value, options, onchange='reloadPage()')
elif hasattr(field, '_property'):
    html = helpers.text_field(field.name, value)
%>
        <div>${html}</div>
        <a href="${url.current(sortname=field.name, sortorder='desc')}" title="Z-A"><span class="ui-icon ui-icon-circle-arrow-s" style="float: right;"></span></a>
        </th>
        %endfor
    <input type="hidden" name="page" value="${h.request.GET.get('page')}" />
    <input type="submit" style="display: none;" />
    </form></tr>
</thead>
<tbody>
<%!
from webhelpers.html.tools import highlight
%>
%for i, row in enumerate(collection.rows):
    <% collection._set_active(row) %>
    <tr class="${i % 2 and 'ui-widget-odd' or 'ui-widget-even'}" id="${row.id}">
        <td class="actions">
##          <a class="entity-url ui-icon ui-icon-circlesmall-plus" href="${'%s/%s' % (url('models', model_name=collection.model.__class__.__name__), row.id)}" target="_blank"></a>
            <a class="entity-url" href="${'%s/%s' % (url('models', model_name=collection.model.__class__.__name__), row.id)}" target="_blank">${i+1}</a>
        </td>
        %for field in collection.render_fields.itervalues():
%if request.GET.get(field.name, ''):
        <td class="normal">${highlight(field.render_readonly(), request.GET.get(field.name, ''))|n}</td>
%else:
        <td class="normal">${field.render_readonly()|n}</td>
%endif
        %endfor
    </tr>
%endfor
</tbody>
<tfoot><tr><td colspan="${1+len(collection.render_fields)}">
<a class="cmd-new ui-widget-header ui-widget-link ui-corner-all" href="${url('models', model_name=collection.model.__class__.__name__) + '/new'}">
    <span class="ui-icon ui-icon-circle-plus"></span>${F_('New')}</a>
<a class="cmd-delete ui-widget-header ui-widget-link ui-corner-all" href="javascript:void(0)" style="display: none;">
    <span class="ui-icon ui-icon-closethick"></span>${F_('Delete')}</a>
<a class="cmd-select ui-widget-header ui-widget-link ui-corner-all" href="javascript:void(0)" style="display: none;">
    <span class="ui-icon ui-icon-power"></span>${F_('Select')}</a>
</td></tr></tfoot>
</table>

## confirm-deletion dialog pattern
<div id="dialog-delete" title="${F_('Confirm operation')}" style="display: none;">
    <p>These items will be permanently deleted and cannot be recovered. Are you sure?</p>
</div>
<script type="text/javascript">
// call to reload the page respecting the filters
function reloadPage() {
    try {
        document.getElementById('filters').submit();
    } catch(x) {}
}

// table rows are selectable
$('table.layout-grid').one('hover', function(){
    var table = $(this);
    var thead = $(this).find('thead');
    var tbody = $(this).find('tbody');
    var tfoot = $(this).find('tfoot');
    table.attr('selectable', 'selectable');
    table.selectable({
        filter: 'tbody >tr',
        cancel: 'td.actions, thead, tfoot, a, img',
        stop: function(){
            // selection changed? -> update available command buttons
            var selection = $(this).find('tr.ui-selected a.entity-url');
            var commands = $(this).find('>tfoot').find('a.cmd-delete, a.cmd-select');
            if (selection.length) commands.show(); else commands.hide();
        }
    });
    // sortable columns
    //$('thead >tr', this).sortable({opacity: 0.6, revert: true});
    // resizable columns
    $('thead >tr >th', this).resizable({
        //containment: 'parent',
        //ghost: true,
        //alsoResize: '.other',
        //autoHide: true
    });
    // scrollable body
    table.before('<div id="counter">Items: ' + tbody.find('tr').length + '</div>');
<%doc>
    tbody.scroll(function(event){
        /*console.info('scrollTop');
        console.log(tbody.scrollTop());
        console.info('height');
        console.log(tbody.height());
        console.info('scrollHeight');
        console.log(tbody);//.scrollHeight);*/
        if (tbody.scrollTop() + tbody.height() >= tbody[0].scrollHeight) {
            var page = Math.floor((tbody.find('tr').length+19)/20)+1;
            // TODO: denormalize!
            if (page > ${collection.pager.page_count}) return;
            var url = '${url('models', model_name=collection.model.__class__.__name__)}';
            $.get(url+'?page='+page, function(data){
                var rows = $(data).find('tbody tr');
                rows.find('a.entity-url').each(function(index){
                    $(this).html(1*parseInt($(this).html())+index);
                });
                //console.log(rows);
                tbody.find('tr:last').after(rows);
                $('#counter').html(tbody.find('tr').length);
            });
        }
    });
</%doc>
    // scrollable tbody. N.B. Opera hangs on bulk row operations...
    if (0) {
    var top = 0;
    var len = tbody.find('tr').length;
    var vis_len = 5; //
    tbody.find('tr').hide();
    tbody.find('tr').slice(top, top+vis_len).show();
    tbody.mousewheel(function(event, delta){
        //window.console.log(delta);
        //if (delta === undefined) delta = 0;
        var new_top = top - delta;
        if (new_top < 0) new_top = 0;
        if (new_top > len-vis_len) new_top = len-vis_len;
        if (top == new_top) return;
        top = new_top;
        window.console.log(top);
        tbody.find('tr').hide();
        tbody.find('tr').slice(top, top+vis_len).show();
        event.preventDefault();
        return false;
    });
    }
    // double clicking the row opens edit dialog
    tbody.find('tr')
    .keyup(function(event){ // TODO: doesn't work...
        if (event.keyCode == 13) {
            $('a.entity-url', this).click();
        }
    }).dblclick(function(){
        $(this).find('a.entity-url').click();
        return false;
    });
});

## feedback from dialogs: to be called from dialogs to refresh the current grid row
## TODO: event instead?
if (!window.updated) {
    window.updated = function(slave) {
        //alert(slave.location.href);
        // get filtered grid for the changed record
        // TODO: can we get rid of url tricking?!
        if (!slave) return;
        var url = slave.location.href.replace(/\/(\d+)(?:\/\w+)?/, '?id=$1');
        var id = url.replace(/.*\?id=(\d+)/, '$1');
        var row = $('#'+id);
        // TODO: find the right table!
        // $('a.entity-url[href='url']').closest('tr')...
        if (!row.length) {
            // replace master table row with new content
            reloadPage();
            slave.close();
            $.jGrowl('Created!');
            return;
        }
        $.get(url, function(text) {
            // replace master table row with new content
            row.html($(text).find('tbody >tr').html());
            // ...and close the slave window
            slave.close();
            $.jGrowl('Updated!');
        });
    }
}

<%doc>
// entity links open edit dialog
$('a.entity-url').live('click', function(){
    // TODO: mark this row as selected
    //$(this).closest('tr').addClass('ui-selected');
    var url = $(this).attr('href');
    // TODO: /edit is just a good guess here
    var wnd = window.open(url + '/edit', '', 'width=520');//,status=true,menubar=false,scrollbars=true,resizable=false,dependent=true');
    return false;
});

// new buttons open new dialog
$('a.cmd-new').live('click', function(){
    var url = $(this).attr('href');
    var wnd = window.open(url, '', 'width=520,status=true,menubar=false,scrollbars=true,resizable=false,dependent=true');
    // TODO: propagate current id to subordinate relations!
    return false;
});
</%doc>

// delete buttons delete selected rows after confirmation
$('a.cmd-delete').live('click', function(){
    // get the closest table
    var selected = $(this).closest('table');
    //if (!selected.length)
    //  selected = $('table');
    // fetch entities URLs from selected rows
    selected = selected.find('tr.ui-selected a.entity-url');
    if (selected.length) {
        // confirm operation
        $('#dialog-delete').dialog({
            bgiframe: true,
            resizable: false,
            modal: true,
            // TODO: i18n
            buttons: {
                Cancel: function() {
                    $(this).dialog('close');
                },
                'Delete selected items': function() {
                    $(this).dialog('close');
                    // delete selected records
                    selected.each(function(){
                        var self = this;
                        var url = $(this).attr('href');
                        $.post(url, {_method: 'DELETE'}, function(text){
                            // remove the row
                            $(self).closest('tr').remove();
                        });
                    });
                }
            }
        });
    }
    return false;
});

// select buttons push the selected entities back to the caller window
$('a.cmd-select').live('click', function(){
    var selected = $('table').find('tr.ui-selected td.actions a.entity-url');
    return false;
});

</script>
