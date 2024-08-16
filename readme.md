### DataCollection: System Metrics Collector

```markdown
# System Monitoring Suite

This project includes three programs that work together to monitor system metrics, store data, and visualize it.

## Programs

1. **DataCollection: System Metrics Collector**
   - Collects CPU usage, memory usage, RAM usage, disk usage, and disk space.
   - Sends this data to a REST service every hour.

2. **API: REST Service**
   - Receives data from Program #1.
   - Stores the data in a PostgreSQL database.

3. **Renderer: Data Visualization**
   - Fetches data from the PostgreSQL database.
   - Renders graphical representations of the collected metrics using matplotlib.

## Setup

### DataCollection: System Metrics Collector

1. Navigate to the `DataCollection` directory.
2. Install dependencies:
   ```bash
   poetry install
   ```
3. Run the collector:
   ```bash
   python collector.py
   ```

### API: REST Service

1. Navigate to the `API` directory.
2. Install dependencies:
   ```bash
   poetry install
   ```
3. Ensure PostgreSQL is running and update the database connection string in `api.py`.
4. Run the REST service:
   ```bash
   python api.py
   ```

### Renderer: Data Visualization

1. Navigate to the `Renderer` directory.
2. Install dependencies:
   ```bash
   poetry install
   ```
3. Run the data visualization:
   ```bash
   python renderer.py
   ```

## Database Schema

The PostgreSQL database should contain a table named `system_data` with the following schema:

```sql
CREATE TABLE system_data (
    id SERIAL PRIMARY KEY,
    ip_address VARCHAR(45),
    timestamp TIMESTAMP,
    cpu_usage FLOAT,
    memory_usage FLOAT,
    ram_usage FLOAT,
    disk_usage FLOAT,
    disk_space FLOAT
);
```

## Notes

- Make sure to replace the database connection details in `API/api.py` and `Renderer/renderer.py` with your actual PostgreSQL credentials.
- Programs should be run in the order: API (REST Service) -> DataCollection (Collector) -> Renderer (Renderer).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
```
