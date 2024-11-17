# A sample image(csv format) processing project using Python

A sample project which does the following:

- Loads a sample image data to the database
- Exposes an API to filter the image data based on depth range and returns the filtered image in jpeg format
- The image size is relatively big. Hence, there is a need to resize the image width to 150 instead of 200. 
- The resized image has to be stored in a database. 
- An API is required to request image frames based on depth_min and depth_max.   
- Apply a custom color map to the generated frames. 

---

## Table of Contents
- [A sample image(csv format) processing project using Python](#a-sample-imagecsv-format-processing-project-using-python)
  - [Table of Contents](#table-of-contents)
  - [Technologies](#technologies)
  - [APIs](#apis)
  - [How to run](#how-to-run)
    - [Prerequisites](#prerequisites)
    - [ToDo](#todo)
  - [Internal Workings](#internal-workings)
---

## Technologies

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Docker

---

## APIs

- `GET /image/{image_data_id}?depth_min={depth_min}&depth_max={depth_max}`
- `GET /health/`

Example:
- `http://13.126.174.40/image/1?depth_min=9000&depth_max=9500`
* This API returns the image frame based on the depth_min and depth_max.
* If depth_min or depth_max is not provided, the default values are applied.
* The image frame is returned in jpeg format.
* The image is filtered based on the depth_min and depth_max.

---

## How to run
- Run the docker compose using `make run`

### Prerequisites

- Python
- Docker
- Make
- Postgres

### ToDo

- Add unit tests
- Add logging
- Add metrics

---

## Internal Workings
- The sample image data is resized to width of 150 and stored in the database as bytes of numpy array in float32 format. This reduces the overhead of storing and retrieving the image using native python datatypes such as list and integers.([utils/fixtures/image_fixtures.py](utils/fixtures/image_fixtures.py))
- When API gets called, the image data is retrieved from the database and processed to get the image frame based on the depth_min and depth_max and converted to jpeg format and returned.([services/image_processing/processor.py](src/services/image_processing/processor.py))
- File Processor is used to convert csv file to numpy array and store in the database.([src/services/image_processing/file_processors.py](src/services/image_processing/file_processors.py)). If any other file format is required, the file processor can be extended to load the data in the required format.
- Resizing of the image is done using `scikit-image` library([src/services/image_processing/processor.py](src/services/image_processing/processor.py#L38)). Various interpolation modes are supported([src/services/image_processing/constants.py](src/services/image_processing/constants.py#L4)).
- Custom color map([src/services/image_processing/constants.py](src/services/image_processing/constants.py#L14)) is applied to the filtered image.
- Database is separated from the image processing logic. This helps in decoupling the business logic from the persistence logic.
- Any database can be used by implementing the `ImageDBService` class. ([src/services/image_db_service.py](src/services/image_db_service.py)).
- APIs are written using FastAPI. Available under [src/api/routers/image_router.py](src/api/routers/image_router.py). Database session is obtained using `get_db` function [src/db/database.py](src/db/database.py) and passed to the service layer.
- Postgres database is selected for ability to stream bytes data in chunks if input data is large.