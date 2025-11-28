from extensions import db
from models import City
from sqlalchemy import func


def calc_city_optimized():
    results = (
        db.session.query(City.city_name, func.avg(City.temperature).label("avg_temp"))
        .group_by(City.city_name)
        .all()
    )
    return [
        {"city": city, "avg_temp": round(avg_temp, 2)} for city, avg_temp in results
    ]


def calc_city_unoptimized():
    cities = [city[0] for city in db.session.query(City.city_name).distinct().all()]
    results = []
    for city_name in cities:
        qs = db.session.query(City).filter(City.city_name == city_name).all()
        total_temp = sum(city_data.temperature for city_data in qs)
        avg_temp = total_temp / len(qs) if qs else 0
        results.append({"city": city_name, "avg_temp": round(avg_temp, 2)})
    return results


def calc_citysemioptimized():
    cities = [city[0] for city in db.session.query(City.city_name).distinct().all()]
    results = []
    for city_name in cities:
        avg_temp = (
            db.session.query(func.avg(City.temperature))
            .filter(City.city_name == city_name)
            .scalar()
        )
        results.append({"city": city_name, "avg_temp": round(avg_temp or 0, 2)})
    return results
