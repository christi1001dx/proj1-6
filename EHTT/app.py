from flask import Flask
from flask import session,url_for, request, redirect, render_template
from pymongo import MongoClient
import erutil, mangodb
