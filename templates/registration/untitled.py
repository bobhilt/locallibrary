{% extends "base_generic.html" %}

{% block content %}

  <h1>Thank you. Your password has been changed.</h1>
  <p><a href="{% url 'login' %}">Login again?</a></p>
{% endblock content %}
