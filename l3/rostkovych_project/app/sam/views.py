from collections import defaultdict
from flask import Blueprint,flash, request, render_template,redirect ,url_for, make_response, session;
from .forms import ReviewForm, Todo
from datetime import datetime
from flask_login import current_user
import json
import os
from app import db

from .models import Review
from . import sam


@sam.route('/review', methods=["POST","GET"])
def review():
   review_form = ReviewForm()
   
   if review_form.validate_on_submit():
    name = review_form.name.data
    review = review_form.review.data
    rating = review_form.rating.data
    new = Review(name=name,rating=rating,review=review)
    db.session.add(new)
    db.session.commit()
    flash("Відгук надіслано", category="success")
   review_list =db.session.query(Review).all()
   return render_template("review.html",form = review_form, list=review_list)
