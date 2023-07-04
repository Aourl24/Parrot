{%extend 'base.html'%}
{% load crispy_forms_tags %}
<body>
<form>
{{form|crispy}}
</form>
</body>