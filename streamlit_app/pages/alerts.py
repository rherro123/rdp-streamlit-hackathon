alert_threshold = 7
alert_severity_map = {7: "#F64F4F", 6: "#EF4040", 5: "#D12929", 4: "#D52D2D", 3: "#B52828", 2: "#901717", 1: "#650505"}

def flag_hot_sku(row):
    days_of_service = row['days_of_service']
    if days_of_service <= alert_threshold:
        color = alert_severity_map[int(days_of_service)]
        return [f'background-color: {color}'] * len(row)
    else:
        return [''] * len(row)