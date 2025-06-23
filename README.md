# SummitFlow

SummitFlow is a productivity application designed to help users stay focused and achieve their goals effectively. It combines tools like a timer, gamification elements, and a distraction-blocking mechanism to ensure users can work productively. 

With SummitFlow, users can:
- Track their productive sessions.
- Block distracting websites during focus time.
- Earn bronze, silver, and gold badges.
- View detailed performance statistics through a personalized dashboard.
- Compete with others via a leaderboard system.

## Features

### 1. **Timer**
- A simple and intuitive timer to manage productive sessions effectively.

### 2. **Gamification**
- Earn badges (Bronze, Silver, Gold) based on achievements.
- Compete with others and climb the leaderboard.

### 3. **Website Blocking**
- Blocks specified distracting websites during productive sessions.
- Implemented as a custom Chrome extension for seamless integration.

### 4. **User Dashboard**
- Displays personalized data, including:
  - User's rank, rating, and badges.
  - Bar chart of productive sessions categorized by day, month, or year.
  - Leaderboard to compare productivity metrics with other users.

### 5. **Backend Integration**
- Built with Django for robust backend support.
- Uses MySQL for efficient data storage and management.

## Tech Stack

### Frontend
- **HTML**: Structure of the user interface.
- **CSS**: Styling and design elements.
- **JavaScript**: Interactive functionalities and Chrome extension development.

### Backend
- **Django**: Backend framework for handling server-side logic.

### Database
- **MySQL**: Relational database management system for storing user data.

## Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Kaushikdsai/Summit-flow.git
   cd Summit-flow
   ```

2. **Set Up the Backend**
   - Install dependencies:
     ```bash
     pip install -r requirements.txt
     ```
   - Apply migrations:
     ```bash
     python manage.py migrate
     ```
   - Start the development server:
     ```bash
     python manage.py runserver
     ```

3. **Set Up the Frontend**
   - Open the `index.html` file in your preferred browser to access the app interface.

4. **Set Up Chrome Extension**
   - Navigate to Chrome's extensions settings by entering `chrome://extensions/` in the address bar.
   - Enable **Developer Mode** by toggling the switch in the top-right corner.
   - Click **Load unpacked** and select the `chrome-extension` folder in the project.
   - Ensure the **service worker** is active by checking the background scripts in the extension details.
   - Grant the necessary permissions if prompted.
   - Verify that the extension appears in the list of Chrome extensions.

## Usage

1. Start a productive session using the timer.
2. Monitor your progress through the dedicated progress page, featuring gamification elements and an integrated timer.
3. Block distracting websites to stay focused.
4. Earn badges and climb the leaderboard based on achievements.

## Future Enhancements
- Add support for custom themes.
- Implement AI features to provide personalized productivity recommendations, such as session planning and distraction pattern analysis.
- Integrate more gamification features, like streak tracking.
- Mobile app version for increased accessibility.

## Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Commit your changes and push to the branch.
4. Submit a pull request for review.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

**SummitFlow** - Your partner in productivity and focus. Let's climb the summit of success together!
