hods=['POST']
# def predict():
#     check_in = request.form['check_in']
#     check_out = request.form['check_out']
#     room_type = request.form['type_of_room']
#     guests = int(request.form['guests'])

#     # Load the model
#     rf, le = joblib.load('random_forest_model.pkl')

#     # Feature engineering
#     booking_lead_time = (pd.to_datetime(check_in) - pd.Timestamp.now()).days
#     stay_duration = (pd.to_datetime(check_out) - pd.to_datetime(check_in)).days
#     room_type_encoded = le.transform([room_type])[0]

#     # Predict
#     features = [[booking_lead_time, stay_duration, room_type_encoded, guests]]
#     prediction = rf.predict(features)

#     # Interpret result
#     result = "Available" if prediction[0] == 1 else "Not Available"
#     return render_template('prediction.html', result=result)

# def train_random_forest():
#     conn = get_db_connection()
#     query = "SELECT check_in, check_out, type_of_room, guests FROM bookings"
#     data = pd.read_sql(query, conn)
#     conn.close()

#     # Preprocessing
#     data['booking_lead_time'] = (pd.to_datetime(data['check_in']) - pd.Timestamp.now()).dt.days
#     data['stay_duration'] = (pd.to_datetime(data['check_out']) - pd.to_datetime(data['check_in'])).dt.days
#     le = LabelEncoder()
#     data['type_of_room_encoded'] = le.fit_transform(data['type_of_room'])

#     # Features and labels
#     X = data[['booking_lead_time', 'stay_duration', 'type_of_room_encoded', 'guests']]
#     y = (data['stay_duration'] <= 10).astype(int)  # Example: Label rooms as available if stay is <=10 days

#     # Train model
#     rf = RandomForestClassifier(n_estimators=100, random_state=42)
#     rf.fit(X, y)

#     # Save model
#     joblib.dump((rf, le), 'random_forest_model.pkl')
#     print("Model trained and saved!")