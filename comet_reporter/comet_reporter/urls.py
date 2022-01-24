from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # path('admin/', admin.site.urls),
    path("api/historicals/",include("historicals.urls")),
    path("api/iterations/",include("iterations.urls")),
    path("api/orders/",include("orders.urls")),
    path("api/trades/",include("trades.urls")),
    path("api/errors/",include("errors.urls"))
]

