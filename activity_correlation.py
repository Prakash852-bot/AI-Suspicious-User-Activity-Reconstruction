
import pandas as pd


def detect_suspicious_activity(timeline):

    suspicious_events = []

    # Check each user separately
    users = timeline["user"].unique()

    for user in users:

        user_events = timeline[
            timeline["user"] == user
        ].sort_values("timestamp")

        # Find successful login events
        login_events = user_events[
            user_events["action"] == "login_success"
        ]

        for _, login in login_events.iterrows():

            start_time = login["timestamp"]

            # Set a 30-minute time window
            end_time = start_time + pd.Timedelta(minutes=30)

            # Find sensitive file access after login
            file_events = user_events[
                (user_events["action"] == "sensitive_file_access") &
                (user_events["timestamp"] >= start_time) &
                (user_events["timestamp"] <= end_time)
            ]

            # Find USB connections after login
            usb_events = user_events[
                (user_events["action"] == "usb_connected") &
                (user_events["timestamp"] >= start_time) &
                (user_events["timestamp"] <= end_time)
            ]

            # Check whether both activities occurred
            if not file_events.empty and not usb_events.empty:

                for _, file_event in file_events.iterrows():

                    for _, usb_event in usb_events.iterrows():

                        # Confirm the file event happened before USB connection
                        if file_event["timestamp"] <= usb_event["timestamp"]:

                            suspicious_events.append({
                                "user": user,
                                "login_time": start_time,
                                "file_access_time": file_event["timestamp"],
                                "file_name": file_event["object"],
                                "usb_connection_time": usb_event["timestamp"],
                                "usb_device": usb_event["object"],
                                "time_window": "30 minutes",
                                "finding": "Correlated activity sequence detected",
                                "status": "Requires investigation"
                            })

    return pd.DataFrame(suspicious_events)

