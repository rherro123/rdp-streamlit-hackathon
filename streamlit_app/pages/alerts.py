alert_threshold = 7
alert_severity_map = {7: "#E2CE1E", 6: "#E2CE1E", 5: "#FD6104", 4: "#FD6104", 3: "#FD0404", 2: "#FD0404", 1: "#FD0404"}

def flag_hot_sku(row):
    days_of_service = row['Days of Service']
    if days_of_service <= alert_threshold:
        color = alert_severity_map[int(days_of_service)]
        return [f'background-color: {color}'] * len(row)
    else:
        return [''] * len(row)