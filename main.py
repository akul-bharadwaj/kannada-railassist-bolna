from typing import Dict, List

from fastapi import FastAPI
from pydantic import BaseModel, Field


app = FastAPI(
    title="Kannada RailAssist",
    description="FastAPI backend for a Kannada voice-agent train availability demo using Bolna AI.",
    version="1.0.0",
)


class TrainSearchRequest(BaseModel):
    source_city: str = Field(..., examples=["Bengaluru"])
    destination_city: str = Field(..., examples=["Hubballi"])
    journey_date: str = Field(..., examples=["2026-06-15"])
    train_preference: str = Field(default="any", examples=["Vande Bharat"])
    travel_class: str = Field(default="any", examples=["CC"])


CITY_TO_STATION: Dict[str, str] = {
    "bengaluru": "SBC",
    "bangalore": "SBC",
    "yeshwanthpur": "YPR",
    "yesvantpur": "YPR",
    "smvt": "SMVB",
    "sir m visvesvaraya terminal": "SMVB",
    "hubli": "UBL",
    "hubballi": "UBL",
    "dharwad": "DWR",
    "mysuru": "MYS",
    "mysore": "MYS",
}


STATION_DISPLAY_NAMES: Dict[str, str] = {
    "SBC": "Bengaluru",
    "YPR": "Yeshwanthpur",
    "SMVB": "SMVT Bengaluru",
    "UBL": "Hubballi",
    "DWR": "Dharwad",
    "MYS": "Mysuru",
}


MOCK_TRAINS: Dict[str, List[Dict[str, object]]] = {
    "SBC-UBL": [
        {
            "train_number": "20661",
            "train_name": "KSR Bengaluru - Dharwad Vande Bharat Express",
            "source_station": "SBC",
            "destination_station": "UBL",
            "departure_time": "05:45",
            "arrival_time": "11:30",
            "duration": "5h 45m",
            "classes_available": ["CC", "EC"],
            "booking_status": "Available - CC 42 seats, EC 12 seats",
        },
        {
            "train_number": "17391",
            "train_name": "SBC UBL Express",
            "source_station": "SBC",
            "destination_station": "UBL",
            "departure_time": "22:15",
            "arrival_time": "06:40",
            "duration": "8h 25m",
            "classes_available": ["SL", "3A", "2A"],
            "booking_status": "Available - SL 86 seats, 3A 21 seats",
        },
    ],
    "SBC-DWR": [
        {
            "train_number": "20661",
            "train_name": "KSR Bengaluru - Dharwad Vande Bharat Express",
            "source_station": "SBC",
            "destination_station": "DWR",
            "departure_time": "05:45",
            "arrival_time": "12:10",
            "duration": "6h 25m",
            "classes_available": ["CC", "EC"],
            "booking_status": "Available - CC 38 seats, EC 10 seats",
        },
        {
            "train_number": "16589",
            "train_name": "Rani Chennamma Express",
            "source_station": "SBC",
            "destination_station": "DWR",
            "departure_time": "23:00",
            "arrival_time": "07:25",
            "duration": "8h 25m",
            "classes_available": ["SL", "3A", "2A", "1A"],
            "booking_status": "RAC 14 in 3A, Available in SL",
        },
    ],
    "UBL-SBC": [
        {
            "train_number": "20662",
            "train_name": "Dharwad - KSR Bengaluru Vande Bharat Express",
            "source_station": "UBL",
            "destination_station": "SBC",
            "departure_time": "14:05",
            "arrival_time": "19:45",
            "duration": "5h 40m",
            "classes_available": ["CC", "EC"],
            "booking_status": "Available - CC 35 seats, EC 8 seats",
        },
        {
            "train_number": "17392",
            "train_name": "UBL SBC Express",
            "source_station": "UBL",
            "destination_station": "SBC",
            "departure_time": "21:00",
            "arrival_time": "05:30",
            "duration": "8h 30m",
            "classes_available": ["SL", "3A", "2A"],
            "booking_status": "Available - SL 74 seats, 3A 18 seats",
        },
    ],
    "MYS-SBC": [
        {
            "train_number": "12008",
            "train_name": "Shatabdi Express",
            "source_station": "MYS",
            "destination_station": "SBC",
            "departure_time": "14:15",
            "arrival_time": "16:25",
            "duration": "2h 10m",
            "classes_available": ["CC", "EC"],
            "booking_status": "Available - CC 55 seats, EC 16 seats",
        },
        {
            "train_number": "12614",
            "train_name": "Tippu Express",
            "source_station": "MYS",
            "destination_station": "SBC",
            "departure_time": "11:30",
            "arrival_time": "14:00",
            "duration": "2h 30m",
            "classes_available": ["2S", "CC"],
            "booking_status": "Available - 2S 120 seats, CC 28 seats",
        },
    ],
}


def clean_input(value: str) -> str:
    if value is None:
        return ""

    cleaned = str(value).strip()

    # Remove wrapper braces added by some tool-calling systems
    cleaned = cleaned.strip("{}")

    # Remove accidental quotes/spaces
    cleaned = cleaned.strip().strip('"').strip("'").strip()

    return cleaned


def normalize_city_or_station(value: str) -> str:
    cleaned_raw = clean_input(value)
    cleaned_value = " ".join(cleaned_raw.lower().split())
    return CITY_TO_STATION.get(cleaned_value, cleaned_raw.upper())


def build_route(source_station: str, destination_station: str) -> Dict[str, str]:
    return {
        "source_station": source_station,
        "source_name": STATION_DISPLAY_NAMES.get(source_station, source_station),
        "destination_station": destination_station,
        "destination_name": STATION_DISPLAY_NAMES.get(destination_station, destination_station),
    }

def filter_trains(
    trains: List[Dict[str, object]],
    train_preference: str,
    travel_class: str,
) -> List[Dict[str, object]]:
    preference = clean_input(train_preference).lower()
    requested_class = clean_input(travel_class).upper()

    if preference in ["", "any", "none", "null"]:
        preference = "any"

    if requested_class in ["", "ANY", "NONE", "NULL"]:
        requested_class = "ANY"

    filtered_trains = trains
    if preference and preference != "any":
        preference_matches = [
            train for train in filtered_trains if preference in str(train["train_name"]).lower()
        ]
        if preference_matches:
            filtered_trains = preference_matches

    if requested_class and requested_class != "ANY":
        class_matches = [
            train
            for train in filtered_trains
            if requested_class in train["classes_available"]
        ]
        if class_matches:
            filtered_trains = class_matches

    return filtered_trains

def is_any(value: str) -> bool:
    cleaned = clean_input(value).lower()
    return cleaned in ["", "any", "none", "null"]

def format_train_options(trains: List[Dict[str, object]]) -> str:
    train_names = [str(train["train_name"]) for train in trains]

    if len(train_names) == 1:
        return train_names[0]

    if len(train_names) == 2:
        return f"{train_names[0]} ಮತ್ತು {train_names[1]}"

    return ", ".join(train_names[:-1]) + f" ಮತ್ತು {train_names[-1]}"

def format_class_options(classes: List[str]) -> str:
    class_display = {
        "CC": "Chair Car",
        "EC": "Executive Chair Car",
        "SL": "Sleeper",
        "3A": "3A",
        "2A": "2A",
        "1A": "1A",
        "2S": "Second Sitting",
    }

    readable_classes = [class_display.get(cls, cls) for cls in classes]

    if len(readable_classes) == 1:
        return readable_classes[0]

    if len(readable_classes) == 2:
        return f"{readable_classes[0]} ಅಥವಾ {readable_classes[1]}"

    return ", ".join(readable_classes[:-1]) + f" ಅಥವಾ {readable_classes[-1]}"

@app.get("/")
def health_check() -> Dict[str, str]:
    return {
        "service": "Kannada RailAssist",
        "status": "running",
        "docs": "/docs",
    }


@app.post("/train-search")
def train_search(request: TrainSearchRequest) -> Dict[str, object]:
    print("BOLNA REQUEST:", request.model_dump())
    source_station = normalize_city_or_station(request.source_city)
    destination_station = normalize_city_or_station(request.destination_city)
    route_key = f"{source_station}-{destination_station}"
    route = build_route(source_station, destination_station)

    if route_key not in MOCK_TRAINS:
        voice_response = (
            "ಕ್ಷಮಿಸಿ, ಈ route ಗೆ demo data ಲಭ್ಯವಿಲ್ಲ. "
            "ನೀವು Bengaluru to Hubballi ಅಥವಾ Bengaluru to Dharwad try ಮಾಡಬಹುದು."
        )

        return {
            "success": False,
            "response": voice_response,
            "message": voice_response,
            "voice_response": voice_response,
            "message_for_voice_agent": voice_response,
        }

    trains = filter_trains(
        MOCK_TRAINS[route_key],
        request.train_preference,
        request.travel_class,
    )

    if not trains:
        voice_response = (
            f"ಕ್ಷಮಿಸಿ, {route['source_name']} ಇಂದ {route['destination_name']} ಗೆ "
            f"{request.journey_date} ರಂದು matching train ಲಭ್ಯವಿಲ್ಲ. "
            "ನೀವು ಬೇರೆ train ಅಥವಾ class try ಮಾಡಬಹುದು."
        )

        return {
            "success": False,
            "response": voice_response,
            "message": voice_response,
            "voice_response": voice_response,
            "message_for_voice_agent": voice_response,
        }

    # Step 1: If train preference is not selected, list available trains
    if is_any(request.train_preference):
        train_options = format_train_options(trains)

        voice_response = (
            f"{request.journey_date} {route['source_name']} ಇಂದ "
            f"{route['destination_name']} ಗೆ {len(trains)} trains available ಇದೆ: "
            f"{train_options}. ನಿಮಗೆ ಯಾವ train ಬೇಕು?"
        )

        return {
            "success": True,
            "stage": "ask_train_preference",
            "response": voice_response,
            "message": voice_response,
            "voice_response": voice_response,
            "message_for_voice_agent": voice_response,
            "available_trains": trains,
        }

    # Step 2: If train is selected but class is not selected, ask class
    if is_any(request.travel_class):
        top_train = trains[0]
        available_classes = top_train["classes_available"]
        class_options = format_class_options(available_classes)

        voice_response = (
            f"{top_train['train_name']} ನಲ್ಲಿ {class_options} available ಇದೆ. "
            "ನಿಮಗೆ ಯಾವ class ಬೇಕು?"
        )

        return {
            "success": True,
            "stage": "ask_travel_class",
            "response": voice_response,
            "message": voice_response,
            "voice_response": voice_response,
            "message_for_voice_agent": voice_response,
            "selected_train": top_train,
            "available_classes": available_classes,
        }

    # Step 3: Train and class selected, give final availability
    top_train = trains[0]

    voice_response = (
        f"{request.journey_date} {route['source_name']} ಇಂದ "
        f"{route['destination_name']} ಗೆ {top_train['train_name']} available ಇದೆ. "
        f"Train number {top_train['train_number']}. "
        f"Departure {top_train['departure_time']}, arrival {top_train['arrival_time']}. "
        f"{top_train['booking_status']}. "
        "ನಿಮಗೆ booking link share ಮಾಡಲಾ?"
    )

    return {
        "success": True,
        "stage": "final_availability",
        "response": voice_response,
        "message": voice_response,
        "voice_response": voice_response,
        "message_for_voice_agent": voice_response,
        "selected_train": top_train,
    }
