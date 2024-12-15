# /backend/analytics.py
def get_template_publish_data():
    # Mock data: In a real scenario, you would query the database or analytics tables.
    return {
        "web_scraper": {"count": 25, "revenue": 199.99},
        "tab_manager": {"count": 15, "revenue": 99.99}
    }

def get_popular_templates(db):
    # Enhanced to include the count and revenue for each template
    publish_data = get_template_publish_data()

    results = []
    for template_name, stats in publish_data.items():
        results.append({
            "template": template_name,
            "count": stats["count"],
            "revenue": stats["revenue"]
        })
    return results
