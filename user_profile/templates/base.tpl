<!DOCTYPE html>
{% load staticfiles %}
<html lang="en">
  <head>
  {% block stylesheets %}
    <link rel="stylesheet" href="{% static 'style.css' %}">
  {% endblock stylesheets %}
  </head>
  <body>
    <section id="content">
      {% block content %}{% endblock %}
    </section>
  </body>
</html>
