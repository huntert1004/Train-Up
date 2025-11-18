# TrainUp — Local Workout Tracker (PyQt5)

TrainUp is a lightweight, offline workout tracking application built with Python and PyQt5.
It allows you to log training sessions, review your workout history, and visualize progress over time through Matplotlib charts.
All data is stored locally in a CSV file for simplicity, portability, and full user control.

## Features

### Add Workout Sessions
- Add one or multiple exercises per session
- Input fields: Exercise name, Reps, Sets, Weight (lbs)
- Automatic timestamps
- Input validation for incorrect or missing data

### Modern User Interface
- Card-style layout for clean organization
- Scrollable entry form
- Wide, easy-to-read fields
- Consistent styling and spacing

### Workout History Table
- Displays all logged workout sessions
- Alternating row colors for readability
- Hover highlighting for easier navigation
- Stretching columns for a better layout
- Ability to delete selected entries
- Automatic table refresh after saving

### Progress Visualization
- Creates line graphs showing training volume over time
- Volume is calculated using:

  Volume = Weight × Reps × Sets

- Only plots exercises logged more than once
- Useful for tracking long-term progression

### Local CSV Storage
All workout data is stored in:

```
workout_log.csv
```

The schema is:

| Timestamp | Exercise | Reps | Sets | Weight |
|----------|----------|------|------|--------|

No database setup is required.

## Project Structure

```
TrainUp/
│── main.py
│── workout_log.csv
│── README.md
└── requirements.txt
```
## Python Version
```
Python Version: Python 3.11.7
```
## Installation

Clone the repository:

```
git clone https://github.com/YOUR_USERNAME/TrainUp.git
cd TrainUp
```

Install dependencies:

```
pip install pyqt5 matplotlib
```

Run the application:

```
python main.py
```

## Technologies Used

- Python 3
- PyQt5 (GUI)
- Matplotlib (charts)
- CSV (data storage)

## Future Enhancements

- Dark mode
- PR tracking (1RM estimation and history)
- Searchable/filterable workout table
- Export to PDF
- A dashboard with weekly or monthly statistics
- Ability to import/export full logs
- Integrated rest timer

## Contributing

Contributions and suggestions are welcome.
Feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License.