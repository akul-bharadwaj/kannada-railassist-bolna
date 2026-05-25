# Kannada RailAssist

Kannada RailAssist is a FastAPI backend demo for a Kannada voice-agent train availability flow using Bolna AI. It accepts train search requests from a Bolna voice agent, normalizes common Karnataka city and station names, and returns short, voice-friendly responses that can be spoken directly by the agent.

This project is designed as a job-application demo to showcase:

- Kannada voice-agent flow design
- Bolna AI tool/function calling
- Dynamic slot filling for train preference and travel class
- FastAPI backend integration
- Mock train availability responses suitable for a voice interface

## Project Overview

The backend exposes one main endpoint:

```text
POST /train-search
```

The API supports a dynamic conversation flow:

1. User provides source city, destination city, and journey date.
2. If train preference is missing, the backend lists available trains and asks the user to choose one.
3. If travel class is missing, the backend lists available classes for the selected train and asks the user to choose one.
4. Once train and class are selected, the backend returns the final availability response.

Supported demo routes:

- Bengaluru to Hubballi
- Bengaluru to Dharwad
- Hubballi to Bengaluru
- Mysuru to Bengaluru

The Bengaluru to Hubballi and Bengaluru to Dharwad routes include a Vande Bharat train.

> This is a demo train availability assistant. It does not perform official IRCTC booking.

## Architecture

```text
Kannada Voice Input
        |
        v
Bolna AI Voice Agent
        |
        | Calls train_search tool
        v
FastAPI Backend
        |
        | Normalizes cities/stations
        | Applies dynamic slot-filling logic
        v
Mock Train Availability Data
        |
        v
Voice-friendly response
        |
        v
Bolna speaks response to user
```


## Demo Recording with [Bolna AI Platform](https://platform.bolna.ai/)

<video src="https://youtu.be/A_COM-ac1lc" controls width="800"></video>


## Key Files

```text
main.py           FastAPI app, request model, route normalization, mock train data, and dynamic response logic
requirements.txt Python dependencies
.env.example     Example local environment configuration
README.md        Project documentation
```

## Setup Steps

Create and activate a virtual environment:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the app locally:

```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Open the API docs:

```text
http://127.0.0.1:8000/docs
```

## Expose Local Backend for Bolna

Bolna cannot call `127.0.0.1` from your laptop. Use ngrok to expose your local FastAPI server:

```bash
ngrok http 8000
```

Example public endpoint:

```text
https://your-ngrok-url.ngrok-free.dev/train-search
```

Use this public `/train-search` URL inside the Bolna custom function/tool configuration.

## API Request Format

```json
{
  "source_city": "Bengaluru",
  "destination_city": "Hubballi",
  "journey_date": "today",
  "train_preference": "any",
  "travel_class": "any"
}
```

Field meaning:

| Field | Description | Example |
|---|---|---|
| `source_city` | Source city or station name | `Bengaluru` |
| `destination_city` | Destination city or station name | `Hubballi` |
| `journey_date` | Journey date or natural date phrase | `today` |
| `train_preference` | Preferred train name/type, or `any` if unknown | `Vande Bharat`, `Shatabdi`, `any` |
| `travel_class` | Preferred class, or `any` if unknown | `CC`, `EC`, `SL`, `3A`, `any` |

## Dynamic API Examples

### 1. Route Known, Train Preference Missing

Request:

```json
{
  "source_city": "Mysuru",
  "destination_city": "Bengaluru",
  "journey_date": "today",
  "train_preference": "any",
  "travel_class": "any"
}
```

Expected response style:

```json
{
  "success": true,
  "stage": "ask_train_preference",
  "response": "today Mysuru ಇಂದ Bengaluru ಗೆ 2 trains available ಇದೆ: Shatabdi Express ಮತ್ತು Tippu Express. ನಿಮಗೆ ಯಾವ train ಬೇಕು?",
  "message": "today Mysuru ಇಂದ Bengaluru ಗೆ 2 trains available ಇದೆ: Shatabdi Express ಮತ್ತು Tippu Express. ನಿಮಗೆ ಯಾವ train ಬೇಕು?",
  "voice_response": "today Mysuru ಇಂದ Bengaluru ಗೆ 2 trains available ಇದೆ: Shatabdi Express ಮತ್ತು Tippu Express. ನಿಮಗೆ ಯಾವ train ಬೇಕು?",
  "message_for_voice_agent": "today Mysuru ಇಂದ Bengaluru ಗೆ 2 trains available ಇದೆ: Shatabdi Express ಮತ್ತು Tippu Express. ನಿಮಗೆ ಯಾವ train ಬೇಕು?"
}
```

### 2. Train Selected, Class Missing

Request:

```json
{
  "source_city": "Mysuru",
  "destination_city": "Bengaluru",
  "journey_date": "today",
  "train_preference": "Shatabdi",
  "travel_class": "any"
}
```

Expected response style:

```json
{
  "success": true,
  "stage": "ask_travel_class",
  "response": "Shatabdi Express ನಲ್ಲಿ Chair Car ಅಥವಾ Executive Chair Car available ಇದೆ. ನಿಮಗೆ ಯಾವ class ಬೇಕು?",
  "message": "Shatabdi Express ನಲ್ಲಿ Chair Car ಅಥವಾ Executive Chair Car available ಇದೆ. ನಿಮಗೆ ಯಾವ class ಬೇಕು?",
  "voice_response": "Shatabdi Express ನಲ್ಲಿ Chair Car ಅಥವಾ Executive Chair Car available ಇದೆ. ನಿಮಗೆ ಯಾವ class ಬೇಕು?",
  "message_for_voice_agent": "Shatabdi Express ನಲ್ಲಿ Chair Car ಅಥವಾ Executive Chair Car available ಇದೆ. ನಿಮಗೆ ಯಾವ class ಬೇಕು?"
}
```

### 3. Train and Class Selected

Request:

```json
{
  "source_city": "Mysuru",
  "destination_city": "Bengaluru",
  "journey_date": "today",
  "train_preference": "Shatabdi",
  "travel_class": "CC"
}
```

Expected response style:

```json
{
  "success": true,
  "stage": "final_availability",
  "response": "today Mysuru ಇಂದ Bengaluru ಗೆ Shatabdi Express available ಇದೆ. Train number 12008. Departure 14:15, arrival 16:25. Available - CC 55 seats, EC 16 seats. ನಿಮಗೆ booking link share ಮಾಡಲಾ?",
  "message": "today Mysuru ಇಂದ Bengaluru ಗೆ Shatabdi Express available ಇದೆ. Train number 12008. Departure 14:15, arrival 16:25. Available - CC 55 seats, EC 16 seats. ನಿಮಗೆ booking link share ಮಾಡಲಾ?",
  "voice_response": "today Mysuru ಇಂದ Bengaluru ಗೆ Shatabdi Express available ಇದೆ. Train number 12008. Departure 14:15, arrival 16:25. Available - CC 55 seats, EC 16 seats. ನಿಮಗೆ booking link share ಮಾಡಲಾ?",
  "message_for_voice_agent": "today Mysuru ಇಂದ Bengaluru ಗೆ Shatabdi Express available ಇದೆ. Train number 12008. Departure 14:15, arrival 16:25. Available - CC 55 seats, EC 16 seats. ನಿಮಗೆ booking link share ಮಾಡಲಾ?"
}
```

## Bolna AI Function/Tool Configuration

Use the ngrok URL for local testing.

```json
{
  "name": "train_search",
  "description": "Search mock train availability for Kannada RailAssist demo routes.",
  "parameters": {
    "type": "object",
    "properties": {
      "source_city": {
        "type": "string",
        "description": "Source city or station name, for example Bengaluru or Mysuru."
      },
      "destination_city": {
        "type": "string",
        "description": "Destination city or station name, for example Hubballi or Bengaluru."
      },
      "journey_date": {
        "type": "string",
        "description": "Journey date, for example today, tomorrow, or YYYY-MM-DD."
      },
      "train_preference": {
        "type": "string",
        "description": "Preferred train name/type. Use any if the user has not selected a train."
      },
      "travel_class": {
        "type": "string",
        "description": "Preferred travel class. Use any if the user has not selected a class."
      }
    },
    "required": [
      "source_city",
      "destination_city",
      "journey_date"
    ]
  },
  "key": "custom_task",
  "value": {
    "method": "POST",
    "param": {
      "source_city": "source_city",
      "destination_city": "destination_city",
      "journey_date": "journey_date",
      "train_preference": "train_preference",
      "travel_class": "travel_class"
    },
    "url": "https://your-ngrok-url.ngrok-free.dev/train-search",
    "api_token": null,
    "headers": {
      "Content-Type": "application/json"
    }
  }
}
```

Important notes for Bolna:

- Keep only `source_city`, `destination_city`, and `journey_date` as required fields.
- Pass `train_preference` as `any` if the user has not selected a train.
- Pass `travel_class` as `any` if the user has not selected a class.
- If Bolna sends values with braces, such as `{Bengaluru}`, the backend cleans the value before matching.
- The agent prompt should tell Bolna to speak only the `response`, `voice_response`, or `message_for_voice_agent` field from the tool.

## Recommended Bolna Agent Prompt Section

Use this as the conversation-flow section inside the Bolna agent prompt:

```text
Conversation flow:

1. If destination_city is missing, ask: "ನಿಮಗೆ ಯಾವ city ಗೆ travel ಮಾಡಬೇಕು?"

2. If source_city is missing, ask: "ನೀವು ಯಾವ city ಇಂದ travel ಮಾಡ್ತಿದ್ದೀರಾ?"

3. If journey_date is missing, ask: "ನೀವು ಇವತ್ತು travel ಮಾಡಬೇಕಾ ಅಥವಾ ಬೇರೆ date?"

4. Once source_city, destination_city, and journey_date are known, call train_search.

5. If train_preference is missing, pass train_preference as "any".

6. If travel_class is missing, pass travel_class as "any".

7. When calling train_search, pass source_city, destination_city, journey_date, train_preference, and travel_class.

8. After train_search returns, speak only the response field from the tool.

9. If response field is not available, speak only the voice_response field.

10. If voice_response is not available, speak only the message_for_voice_agent field.

11. If the tool response asks the user to choose a train, wait for the user's answer.

12. When the user chooses a train, call train_search again with the same source_city, destination_city, and journey_date, and set train_preference to the selected train.

13. If the tool response asks the user to choose a class, wait for the user's answer.

14. When the user chooses a class, call train_search again with the same source_city, destination_city, journey_date, and train_preference, and set travel_class to the selected class.

15. If user says Vande Bharat, set train_preference as "Vande Bharat".

16. If user says Shatabdi, set train_preference as "Shatabdi Express".

17. If user says Tippu, set train_preference as "Tippu Express".

18. If user says Chair Car, set travel_class as "CC".

19. If user says Executive Chair Car, set travel_class as "EC".

20. If user says Sleeper, set travel_class as "SL".

21. If user says 3A, set travel_class as "3A".

22. If user says any train, set train_preference as "any".

23. If user says any class, set travel_class as "any".

24. After giving final train availability, ask only: "ನಿಮಗೆ booking link share ಮಾಡಲಾ?"

25. Do not invent train names, class options, timings, or seat counts. Use only the tool response.
```

## Sample Kannada Conversation

User:

```text
Naanu Mysuru inda Bengaluru ge ivathu train nodbeku.
```

Agent calls `/train-search` with:

```json
{
  "source_city": "Mysuru",
  "destination_city": "Bengaluru",
  "journey_date": "today",
  "train_preference": "any",
  "travel_class": "any"
}
```

Agent:

```text
today Mysuru ಇಂದ Bengaluru ಗೆ 2 trains available ಇದೆ: Shatabdi Express ಮತ್ತು Tippu Express. ನಿಮಗೆ ಯಾವ train ಬೇಕು?
```

User:

```text
Shatabdi Express
```

Agent calls `/train-search` with:

```json
{
  "source_city": "Mysuru",
  "destination_city": "Bengaluru",
  "journey_date": "today",
  "train_preference": "Shatabdi Express",
  "travel_class": "any"
}
```

Agent:

```text
Shatabdi Express ನಲ್ಲಿ Chair Car ಅಥವಾ Executive Chair Car available ಇದೆ. ನಿಮಗೆ ಯಾವ class ಬೇಕು?
```

User:

```text
Chair Car
```

Agent calls `/train-search` with:

```json
{
  "source_city": "Mysuru",
  "destination_city": "Bengaluru",
  "journey_date": "today",
  "train_preference": "Shatabdi Express",
  "travel_class": "CC"
}
```

Agent:

```text
today Mysuru ಇಂದ Bengaluru ಗೆ Shatabdi Express available ಇದೆ. Train number 12008. Departure 14:15, arrival 16:25. Available - CC 55 seats, EC 16 seats. ನಿಮಗೆ booking link share ಮಾಡಲಾ?
```

## Supported City and Station Normalization

The backend normalizes common names such as:

| Input | Station Code |
|---|---|
| Bengaluru / Bangalore | SBC |
| Yeshwanthpur / Yesvantpur | YPR |
| SMVT / Sir M Visvesvaraya Terminal | SMVB |
| Hubli / Hubballi | UBL |
| Dharwad | DWR |
| Mysuru / Mysore | MYS |

## Unsupported Route Response

If a route is not available in the demo data, the API returns a voice-friendly response like:

```json
{
  "success": false,
  "response": "ಕ್ಷಮಿಸಿ, ಈ route ಗೆ demo data ಲಭ್ಯವಿಲ್ಲ. ನೀವು Bengaluru to Hubballi ಅಥವಾ Bengaluru to Dharwad try ಮಾಡಬಹುದು.",
  "message": "ಕ್ಷಮಿಸಿ, ಈ route ಗೆ demo data ಲಭ್ಯವಿಲ್ಲ. ನೀವು Bengaluru to Hubballi ಅಥವಾ Bengaluru to Dharwad try ಮಾಡಬಹುದು.",
  "voice_response": "ಕ್ಷಮಿಸಿ, ಈ route ಗೆ demo data ಲಭ್ಯವಿಲ್ಲ. ನೀವು Bengaluru to Hubballi ಅಥವಾ Bengaluru to Dharwad try ಮಾಡಬಹುದು.",
  "message_for_voice_agent": "ಕ್ಷಮಿಸಿ, ಈ route ಗೆ demo data ಲಭ್ಯವಿಲ್ಲ. ನೀವು Bengaluru to Hubballi ಅಥವಾ Bengaluru to Dharwad try ಮಾಡಬಹುದು."
}
```

## Limitations

- Uses mock train availability data only.
- Does not connect to IRCTC, NTES, or any live railway API.
- Does not perform ticket booking, payment, OTP, login, CAPTCHA, or passenger-detail collection.
- Does not validate whether the journey date is a real operating day.
- Booking status values are demo strings and may not match real availability.
- Kannada-English mixed speech is supported at a basic demo level.
- This project is intended for demonstrating voice-agent orchestration, not production railway booking.

## Future Improvements

- Add live train search integration when an approved API is available.
- Add stronger Kannada NLP and transliteration support.
- Add better natural date parsing for phrases like "ನಾಳೆ" and "ಮುಂದಿನ ಸೋಮವಾರ".
- Add persistent conversation state for more complex multi-turn flows.
- Add automated tests for supported routes, unsupported routes, train selection, and class selection.
- Add authentication, request logging, and monitoring for production use.
- Add WhatsApp/SMS integration to share a booking link or train summary.

## Demo Positioning

This project demonstrates how a Kannada voice agent can:

- Understand a train-search request in Kannada/Kannada-English speech
- Collect missing travel details conversationally
- Call a backend API using Bolna AI function/tool calling
- Dynamically ask for train preference and travel class
- Return a short voice-friendly response
- Avoid claiming official IRCTC booking or confirmed ticketing
