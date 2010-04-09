# -*- coding: utf-8 -*-
<%!
from formalchemy.ext.pylons.controller import model_url
%>
<% async = request.is_xhr %>
<%def name="h1(title, href=None)">
    <h1 class="ui-widget-header ui-corner-all">
      %if breadcrumb and not async:
        <div class="breadcrumb">
         /${'/'.join([u and '<a href="%s">%s</a>' % (u,n.lower()) or n.lower() for u,n in breadcrumb])|n}
         <a href="/login/signout" style="font-size1:0.7em;font-weight1:normal;text-decoration:none">signout</a>
        </div>
      %endif
      %if href:
        <a href="${href}">${title.title()}</a>
      %else:
        ${title.title()}
      %endif
    </h1>
</%def>
<%def name="buttons()">
    <p class="fa_field">
    %if action == 'show':
      <a class="ui-widget-header ui-widget-link ui-corner-all" href="${h.model_url('edit_%s' % member_name, id=id)}">
        <span class="ui-icon ui-icon-pencil"></span>
        ${F_('Edit')}
      </a>
    %else:
      <a class="ui-widget-header ui-widget-link ui-widget-button ui-corner-all" href="javascript:void(0)" onclick="$(this).closest('form').submit(); return false;">
        <span class="ui-icon ui-icon-${'check' if action != 'confirm' else 'closethick'}"></span>
        ${F_('Save' if action != 'confirm' else 'Delete')}
        <input type="submit" />
      </a>
    %endif
      <a class="ui-widget-header ui-widget-link ui-corner-all" href="${h.model_url(collection_name)}" onclick="if(opener){window.close();return false;}">
        <span class="ui-icon ui-icon-circle-arrow-w"></span>
        ${F_('Cancel')}
      </a>
    </p>
</%def>
%if not async:
<html>
  <head>
    <title>
    ${collection_name.title()}
    </title>
    <link type="text/css" rel="stylesheet" href="${h.url('fa_static', path_info='css/ui-lightness/jquery-ui-1.8rc1.custom.css')}" />
    <link type="text/css" rel="stylesheet" href="${h.url('fa_static', path_info='fa.jquery.min.css')}" />
    <script type="text/javascript" src="${h.url('fa_static', path_info='fa.jquery.min.js')}"></script>
    <style>
## form styles
div.ui-admin {
    width: 960px;
    margin-left: auto;
    margin-right: auto;
}
form {
    width: 500px;
    margin: 0 auto;
    padding: 0;
}
div.fa_field {
    margin: 0;
    padding: 1em 0 0;
}
form input, form select {
    width: 100%;
}
form textarea {
    width: 100%;
    height: 20em;
}
form input[type=checkbox] {
    display: inline-block;
    width: 20px;
}
    </style>
## grid styles
    <style>
table.layout-grid >tbody {
    height: 300px;
    overflow-x: hidden;
    overflow-y: scroll;
}
table.layout-grid tr.ui-widget-header th input, table.layout-grid tr.ui-widget-header th select {width:100%;}
table.layout-grid td.actions {
    background: #F6A828; /* TODO: grab from the theme */
    text-align: center;
    vertical-align: middle;
}
table.layout-grid td.actions a {
    display: inline-block;
    opacity: 0.5;
    font-weight: bold;
    color: black;
}
table.layout-grid tr:hover td.actions a {}
table.layout-grid tr.ui-selecting { background: #FECA40; }
table.layout-grid tr.ui-selected { background: #F39814; color: white; }
table.layout-grid td.inline-form >div {
    border: 4px solid gray;
    padding: 10px;
    background: #f0f0f0;
}
table.layout-grid tfoot td {
    padding: 1em 0.3em;
}
strong.highlight {
    background: yellow;
}
    </style>
## setup AJAX
    <script type="text/javascript">
// register global AJAX event handlers
jQuery(document)
.ajaxStart(function(){
    $('#loading').show();
}).ajaxStop(function(){
    $('#loading').hide();
}).ajaxError(function(ev, xhr){
    $.jGrowl(xhr.responseText, {sticky: true});
});
    </script>
  </head>
  <body>
<img id="loading" src="${h.url('fa_static', path_info='loading.gif')}" style="display: none; position: fixed; width: 30px; height: 30px; left: 10px; top: 10px; margin: auto; z-index: 1000;" />
%endif
## dislay c.flash messages
%if getattr(c, 'flash', None):
<script type="text/javascript">
    $.jGrowl('${F_(c.flash)}', {life: 3000, sticky: false, header: ''});
</script>
%endif
<div class="ui-admin ui-widget">
%if is_grid:
    ${h1(model_name)}
    <div class="ui-pager">${pager|n}</div>
    ${fs.render()|n}
## close window upon successful create
<script type="text/javascript">
    // subordinate window reports to master
    if (opener && opener.updated) {
        opener.updated(window);
    }
</script>
%else:
  %if isinstance(models, dict):
    <h1 class="ui-widget-header ui-corner-all">Models</h1>
    %for name in sorted(models):
      <p>
        <a class="ui-state-default ui-corner-all" href="${models[name]}">${name}</a>
      </p>
    %endfor
  %elif not is_grid:
    <h2 class="ui-widget-header ui-corner-all">${fs.model if action != 'new' else action}</h2>
    %if action == 'show':
      <table>
        ${fs.render()|n}
      </table>
      ${buttons()}
## close window upon successful update
<%doc>
<script type="text/javascript">
    // subordinate window reports to master
    if (opener && opener.updated) {
        opener.updated(window);
    }
</script>
</%doc>
    %elif action == 'edit':
      <form action="${h.model_url(member_name, id=id)}" method="POST" enctype="multipart/form-data">
        ${fs.render()|n}
        <input type="hidden" name="_method" value="PUT" />
        ${buttons()}
      </form>
    %elif action == 'confirm':
      <h2 class="ui-widget-header ui-corner-all">${F_('Confirm deletion of this record')}</h3>
      <table>
        ${fs.render()|n}
      </table>
      <form action="${h.model_url(member_name, id=id)}" method="POST" enctype="multipart/form-data">
        <input type="hidden" name="_method" value="DELETE" />
        ${buttons()}
      </form>
    %else:
      <form action="${h.model_url(collection_name)}" method="POST" enctype="multipart/form-data">
        ${fs.render()|n}
        ${buttons()}
      </form>
    %endif
  %endif
%endif
</div>
%if not async:
<script type="text/javascript">
$('select.filter').each(function(){
    var box = $(this);
    // cache options
    var options = box.find('option');
    // create filtering textbox
    var input = $('<input type="text" />');
    input
    // filter is closed on ESC
    .keydown(function(event){
        if (event.keyCode == 27) {
            input.hide().prev().show();
            return false;
        }
    })
    // upon key event we filter selectbox options
    // N.B. filter is case-insensitive and acts as LIKE SQL operator
    .keyup(function(event){
        var value = $(this).val().toLowerCase();
        // clear the box
        box.html('');
        // append only matching options
        options.each(function(){
            var option = $(this);
            if (!value || option.html().toLowerCase().indexOf(value) >= 0)
                box.append(option);
        });
        // user paused typing? -> move focus to the selectbox
        // TODO: how to automatically dropdown the selectbox?
        setTimeout(function(){
            input.hide().prev().show();
            box.focus();//.triggerHandler({type: 'keydown', keyCode: 40, altKey: true, target: box[0], currentTarget: box[0]});
        }, 1500);
    })
    // insert initially hidden textbox before the selectbox
    .hide().insertBefore(box)
    // insert 'Filter' button
    // TODO: may be just image to the right of the selectbox?!
    .before('<a href="javascript:void(0)" style="position1: relative; float1: right; margin-top1: -18px;" onclick="$(this).hide().next().show().focus(); return false;">Filter</a>'); // TODO: i18n
    // user choosed something? -> hide the filter textbox
    box
    .change(function(){
        input.hide().prev().show();
    })
    .keydown(function(event){
        window.console.log(event);
    });
});
$('select[multiple]').attr('title', 'Click to append items...').asmSelect({ // TODO: i18n
    sortable: true,
    //highlight: true,
    addItemTarget: 'top',
    removeLabel: '${F_('remove')}'
});
</script>
</body></html>
%endif
