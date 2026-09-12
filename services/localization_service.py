"""Offline localization for responses built from the verified disease dataset."""

from typing import Dict

LANGUAGE_NAMES = {"en": "English", "te": "Telugu", "hi": "Hindi", "ta": "Tamil", "kn": "Kannada"}

LABELS: Dict[str, Dict[str, str]] = {
    "te": {
        "prevention": "నివారణ", "disease": "వ్యాధి", "category": "వర్గం", "cause": "కారణం",
        "transmission": "వ్యాప్తి", "symptoms": "సాధారణ లక్షణాలు", "medical_note": "వైద్య గమనిక",
        "prevention_heading": "## దీనిని ఎలా నివారించవచ్చు లేదా తగ్గించవచ్చు?",
        "definition_heading": "## ఇది ఏమిటి?", "facts_heading": "## ధృవీకరించిన ఆరోగ్య అవగాహన సమాచారం",
        "facts_intro": "క్రింది అంశాలు అత్యంత సంబంధిత ధృవీకరించిన ఆరోగ్య మూలం నుండి తీసుకోబడ్డాయి:",
        "notice": "**విద్యా సమాచారం:** ఈ సమాచారం సాధారణ ఆరోగ్య అవగాహన కోసం మాత్రమే. ఇది నిర్ధారణ లేదా వ్యక్తిగత వైద్య సలహా కాదు. అర్హత కలిగిన ఆరోగ్య నిపుణుడిని సంప్రదించండి.",
        "greeting": "హాయ్! నేను HealthAware AI. నేను బాగున్నాను, ధన్యవాదాలు. ఈ రోజు మీకు ఎలా సహాయం చేయగలను? లక్షణాలు, నివారణ, పోషణ, మందులు లేదా సాధారణ ఆరోగ్యంపై ప్రశ్నలు అడగండి.",
    },
    "hi": {
        "prevention": "रोकथाम", "disease": "रोग", "category": "श्रेणी", "cause": "कारण",
        "transmission": "संचरण", "symptoms": "सामान्य लक्षण", "medical_note": "चिकित्सीय टिप्पणी",
        "prevention_heading": "## इसे कैसे रोका या कम किया जा सकता है?", "definition_heading": "## यह क्या है?",
        "facts_heading": "## सत्यापित स्वास्थ्य जागरूकता जानकारी", "facts_intro": "नीचे दिए गए तथ्य सबसे प्रासंगिक सत्यापित स्वास्थ्य स्रोत से लिए गए हैं:",
        "notice": "**शैक्षिक सूचना:** यह जानकारी केवल सामान्य स्वास्थ्य जागरूकता के लिए है। यह निदान या व्यक्तिगत चिकित्सा सलाह नहीं है। योग्य स्वास्थ्य पेशेवर से सलाह लें।",
        "greeting": "नमस्ते! मैं HealthAware AI हूं। मैं ठीक हूं, धन्यवाद। आज मैं आपकी कैसे मदद कर सकता हूं? लक्षणों, रोकथाम, पोषण, दवाओं या सामान्य स्वास्थ्य के बारे में पूछें।",
    },
    "ta": {
        "prevention": "தடுப்பு", "disease": "நோய்", "category": "வகை", "cause": "காரணம்",
        "transmission": "பரவல்", "symptoms": "பொதுவான அறிகுறிகள்", "medical_note": "மருத்துவ குறிப்பு",
        "prevention_heading": "## இதை எவ்வாறு தடுக்கலாம் அல்லது குறைக்கலாம்?", "definition_heading": "## இது என்ன?",
        "facts_heading": "## சரிபார்க்கப்பட்ட சுகாதார விழிப்புணர்வு தகவல்", "facts_intro": "பின்வரும் தகவல்கள் மிகவும் பொருத்தமான சரிபார்க்கப்பட்ட சுகாதார மூலத்திலிருந்து எடுக்கப்பட்டவை:",
        "notice": "**கல்வித் தகவல்:** இந்த தகவல் பொதுவான சுகாதார விழிப்புணர்வுக்காக மட்டுமே. இது நோயறிதல் அல்லது தனிப்பட்ட மருத்துவ ஆலோசனை அல்ல. தகுதியான சுகாதார நிபுணரை அணுகவும்.",
        "greeting": "வணக்கம்! நான் HealthAware AI. நான் நலமாக இருக்கிறேன், நன்றி. இன்று உங்களுக்கு எப்படி உதவலாம்? அறிகுறிகள், தடுப்பு, ஊட்டச்சத்து, மருந்துகள் அல்லது பொதுவான சுகாதாரம் பற்றி கேளுங்கள்.",
    },
    "kn": {
        "prevention": "ತಡೆಗಟ್ಟುವಿಕೆ", "disease": "ರೋಗ", "category": "ವರ್ಗ", "cause": "ಕಾರಣ",
        "transmission": "ಹರಡುವಿಕೆ", "symptoms": "ಸಾಮಾನ್ಯ ಲಕ್ಷಣಗಳು", "medical_note": "ವೈದ್ಯಕೀಯ ಟಿಪ್ಪಣಿ",
        "prevention_heading": "## ಇದನ್ನು ಹೇಗೆ ತಡೆಯಬಹುದು ಅಥವಾ ಕಡಿಮೆ ಮಾಡಬಹುದು?", "definition_heading": "## ಇದು ಏನು?",
        "facts_heading": "## ಪರಿಶೀಲಿಸಿದ ಆರೋಗ್ಯ ಜಾಗೃತಿ ಮಾಹಿತಿ", "facts_intro": "ಕೆಳಗಿನ ಅಂಶಗಳನ್ನು ಹೆಚ್ಚು ಸಂಬಂಧಿತ ಪರಿಶೀಲಿಸಿದ ಆರೋಗ್ಯ ಮೂಲದಿಂದ ತೆಗೆದುಕೊಳ್ಳಲಾಗಿದೆ:",
        "notice": "**ಶೈಕ್ಷಣಿಕ ಮಾಹಿತಿ:** ಈ ಮಾಹಿತಿ ಸಾಮಾನ್ಯ ಆರೋಗ್ಯ ಜಾಗೃತಿಗಾಗಿ ಮಾತ್ರ. ಇದು ರೋಗನಿರ್ಣಯ ಅಥವಾ ವೈಯಕ್ತಿಕ ವೈದ್ಯಕೀಯ ಸಲಹೆಯಲ್ಲ. ಅರ್ಹ ಆರೋಗ್ಯ ವೃತ್ತಿಪರರನ್ನು ಸಂಪರ್ಕಿಸಿ.",
        "greeting": "ನಮಸ್ಕಾರ! ನಾನು HealthAware AI. ನಾನು ಚೆನ್ನಾಗಿದ್ದೇನೆ, ಧನ್ಯವಾದಗಳು. ಇಂದು ನಿಮಗೆ ಹೇಗೆ ಸಹಾಯ ಮಾಡಲಿ? ಲಕ್ಷಣಗಳು, ತಡೆಗಟ್ಟುವಿಕೆ, ಪೋಷಣೆ, ಔಷಧಗಳು ಅಥವಾ ಸಾಮಾನ್ಯ ಆರೋಗ್ಯದ ಬಗ್ಗೆ ಕೇಳಿ.",
    },
}

FIELD_TRANSLATIONS: Dict[str, Dict[str, str]] = {
    "te": {
        "Avoid mosquito bites; use recommended preventive medicines when appropriate; early testing": "దోమ కాట్లను నివారించండి; అవసరమైనప్పుడు సిఫార్సు చేసిన నివారణ మందులను ఉపయోగించండి; ముందుగానే పరీక్ష చేయించుకోండి.",
        "Avoid mosquito bites, especially during the day; reduce mosquito breeding sites": "ముఖ్యంగా పగటిపూట దోమ కాట్లను నివారించండి; దోమలు పెరిగే ప్రదేశాలను తగ్గించండి.",
    },
    "hi": {
        "Avoid mosquito bites; use recommended preventive medicines when appropriate; early testing": "मच्छर के काटने से बचें; आवश्यकता होने पर अनुशंसित निवारक दवाओं का उपयोग करें; समय पर जांच कराएं।",
        "Avoid mosquito bites, especially during the day; reduce mosquito breeding sites": "विशेष रूप से दिन में मच्छरों के काटने से बचें; मच्छरों के प्रजनन स्थलों को कम करें।",
    },
    "ta": {
        "Avoid mosquito bites; use recommended preventive medicines when appropriate; early testing": "கொசு கடியைத் தவிர்க்கவும்; தேவையானபோது பரிந்துரைக்கப்பட்ட தடுப்பு மருந்துகளைப் பயன்படுத்தவும்; ஆரம்பத்திலேயே பரிசோதனை செய்யவும்.",
        "Avoid mosquito bites, especially during the day; reduce mosquito breeding sites": "குறிப்பாக பகலில் கொசு கடியைத் தவிர்க்கவும்; கொசுக்கள் பெருகும் இடங்களைக் குறைக்கவும்.",
    },
    "kn": {
        "Avoid mosquito bites; use recommended preventive medicines when appropriate; early testing": "ಸೊಳ್ಳೆ ಕಚ್ಚುವುದನ್ನು ತಪ್ಪಿಸಿ; ಅಗತ್ಯವಿದ್ದಾಗ ಶಿಫಾರಸು ಮಾಡಿದ ತಡೆಗಟ್ಟುವ ಔಷಧಿಗಳನ್ನು ಬಳಸಿ; ಮುಂಚಿತವಾಗಿ ಪರೀಕ್ಷೆ ಮಾಡಿಸಿಕೊಳ್ಳಿ.",
        "Avoid mosquito bites, especially during the day; reduce mosquito breeding sites": "ವಿಶೇಷವಾಗಿ ಹಗಲಿನಲ್ಲಿ ಸೊಳ್ಳೆ ಕಚ್ಚುವುದನ್ನು ತಪ್ಪಿಸಿ; ಸೊಳ್ಳೆಗಳು ಹೆಚ್ಚಾಗುವ ಸ್ಥಳಗಳನ್ನು ಕಡಿಮೆ ಮಾಡಿ.",
    },
}

UI_TRANSLATIONS: Dict[str, Dict[str, str]] = {
    "te": {
        "Language": "భాష", "App": "యాప్", "Consultations": "సంప్రదింపులు",
        "New Consultation": "కొత్త సంప్రదింపు", "Select Consultation": "సంప్రదింపును ఎంచుకోండి",
        "Educational Notice": "విద్యా సమాచారం", "Home": "హోమ్", "AI Healthcare Chat": "AI ఆరోగ్య చాట్",
        "Health Learning": "ఆరోగ్య అభ్యాసం", "Interactive Quizzes": "ఇంటరాక్టివ్ క్విజ్‌లు",
        "Risk Assessment": "ప్రమాద అంచనా", "Myth vs Fact": "అపోహ vs వాస్తవం",
        "Symptom Checker": "లక్షణాల తనిఖీ", "Medications": "మందులు", "Appointments": "అపాయింట్‌మెంట్లు",
        "Healthcare Directory": "ఆరోగ్య డైరెక్టరీ", "Insurance & Billing": "బీమా & బిల్లింగ్",
        "Mental Wellness": "మానసిక ఆరోగ్యం", "Wearable Health": "వేర్‌బుల్ ఆరోగ్యం",
        "Profile": "ప్రొఫైల్", "Settings": "సెట్టింగ్‌లు",
        "Quick Topics — click to ask:": "త్వరిత అంశాలు — అడగడానికి క్లిక్ చేయండి:",
        "Voice / Audio Input": "వాయిస్ / ఆడియో ఇన్‌పుట్",
        "Say hello or ask a health question": "హలో చెప్పండి లేదా ఆరోగ్య ప్రశ్న అడగండి",
        "Health Learning Curriculum": "ఆరోగ్య అభ్యాస పాఠ్యక్రమం",
        "Evidence-grounded, bite-sized lessons to enhance your healthcare literacy and preventive habits.": "మీ ఆరోగ్య అవగాహన మరియు నివారణ అలవాట్లను మెరుగుపరచే ఆధారాలతో కూడిన చిన్న పాఠాలు.",
        "Category": "వర్గం", "Estimated reading time": "అంచనా పఠన సమయం",
        "Lessons": "పాఠాలు", "Lesson": "పాఠం", "Key Takeaways": "ముఖ్యాంశాలు",
        "Mark": "గుర్తించండి", "Completed": "పూర్తయింది", "You have completed this educational module!": "మీరు ఈ విద్యా మాడ్యూల్‌ను పూర్తి చేశారు!",
        "Healthcare education does not substitute for personalized medical check-ups with your physician.": "ఆరోగ్య విద్య మీ వైద్యుని వ్యక్తిగత వైద్య పరీక్షలకు ప్రత్యామ్నాయం కాదు.",
        "Interactive Healthcare Quizzes": "ఇంటరాక్టివ్ ఆరోగ్య క్విజ్‌లు",
        "Test and sharpen your awareness on cardiovascular health, diabetes, preventive immunization, and first aid.": "హృదయ ఆరోగ్యం, మధుమేహం, నివారణ టీకాలు మరియు ప్రథమ చికిత్సపై మీ అవగాహనను పరీక్షించి మెరుగుపరచుకోండి.",
        "Choose Quiz Topic:": "క్విజ్ అంశాన్ని ఎంచుకోండి:", "No questions available for this topic yet.": "ఈ అంశానికి ఇంకా ప్రశ్నలు అందుబాటులో లేవు.",
        "Restart / Load New Questions": "మళ్లీ ప్రారంభించండి / కొత్త ప్రశ్నలు లోడ్ చేయండి", "Submit Quiz Answers": "క్విజ్ సమాధానాలను సమర్పించండి",
        "Topic:": "అంశం:", "Questions:": "ప్రశ్నలు:", "Question": "ప్రశ్న", "Select your answer for question": "ప్రశ్నకు మీ సమాధానాన్ని ఎంచుకోండి",
        "Quiz Results & Explanations": "క్విజ్ ఫలితాలు & వివరణలు", "Correct!": "సరైనది!", "Incorrect": "తప్పు", "Unanswered": "సమాధానం ఇవ్వలేదు", "Correct:": "సరైన సమాధానం:", "Explanation:": "వివరణ:",
        "Diabetes Awareness & Glucose Management": "మధుమేహ అవగాహన & గ్లూకోజ్ నిర్వహణ",
        "Heart Health & Hypertension Awareness": "గుండె ఆరోగ్యం & అధిక రక్తపోటు అవగాహన",
        "Vaccination Concepts & Adult Immunization": "టీకాల భావనలు & పెద్దల టీకాకరణ",
        "Seasonal Respiratory Illness & Prevention": "కాలానుగుణ శ్వాసకోశ అనారోగ్యం & నివారణ",
        "Endocrine Health": "అంతఃస్రావ ఆరోగ్యం", "Cardiovascular": "హృదయ సంబంధిత ఆరోగ్యం", "Preventive Health": "నివారణ ఆరోగ్యం", "Infectious Disease": "సంక్రమణ వ్యాధి",
    },
    "hi": {
        "Language": "भाषा", "App": "ऐप", "Consultations": "परामर्श",
        "New Consultation": "नया परामर्श", "Select Consultation": "परामर्श चुनें",
        "Educational Notice": "शैक्षिक सूचना", "Home": "होम", "AI Healthcare Chat": "AI स्वास्थ्य चैट",
        "Health Learning": "स्वास्थ्य शिक्षा", "Interactive Quizzes": "इंटरैक्टिव क्विज़",
        "Risk Assessment": "जोखिम आकलन", "Myth vs Fact": "मिथक बनाम तथ्य",
        "Symptom Checker": "लक्षण जांच", "Medications": "दवाएं", "Appointments": "अपॉइंटमेंट",
        "Healthcare Directory": "स्वास्थ्य निर्देशिका", "Insurance & Billing": "बीमा और बिलिंग",
        "Mental Wellness": "मानसिक स्वास्थ्य", "Wearable Health": "वियरेबल स्वास्थ्य",
        "Profile": "प्रोफ़ाइल", "Settings": "सेटिंग्स",
        "Quick Topics — click to ask:": "त्वरित विषय — पूछने के लिए क्लिक करें:",
        "Voice / Audio Input": "वॉइस / ऑडियो इनपुट",
        "Say hello or ask a health question": "नमस्ते कहें या स्वास्थ्य प्रश्न पूछें",
        "Health Learning Curriculum": "स्वास्थ्य शिक्षा पाठ्यक्रम",
        "Evidence-grounded, bite-sized lessons to enhance your healthcare literacy and preventive habits.": "आपकी स्वास्थ्य साक्षरता और रोकथाम की आदतों को बेहतर बनाने वाले प्रमाण-आधारित छोटे पाठ।",
        "Category": "श्रेणी", "Estimated reading time": "अनुमानित पढ़ने का समय", "Lessons": "पाठ", "Lesson": "पाठ", "Key Takeaways": "मुख्य बातें",
        "Mark": "चिह्नित करें", "Completed": "पूरा हुआ", "You have completed this educational module!": "आपने यह शैक्षिक मॉड्यूल पूरा कर लिया है!",
        "Healthcare education does not substitute for personalized medical check-ups with your physician.": "स्वास्थ्य शिक्षा आपके चिकित्सक की व्यक्तिगत चिकित्सा जांच का विकल्प नहीं है।",
        "Interactive Healthcare Quizzes": "इंटरैक्टिव स्वास्थ्य क्विज़",
        "Test and sharpen your awareness on cardiovascular health, diabetes, preventive immunization, and first aid.": "हृदय स्वास्थ्य, मधुमेह, निवारक टीकाकरण और प्राथमिक चिकित्सा पर अपनी जागरूकता जांचें और बढ़ाएं।",
        "Choose Quiz Topic:": "क्विज़ विषय चुनें:", "No questions available for this topic yet.": "इस विषय के लिए अभी कोई प्रश्न उपलब्ध नहीं है।", "Restart / Load New Questions": "फिर शुरू करें / नए प्रश्न लोड करें", "Submit Quiz Answers": "क्विज़ उत्तर जमा करें", "Question": "प्रश्न", "Select your answer for question": "प्रश्न के लिए अपना उत्तर चुनें", "Quiz Results & Explanations": "क्विज़ परिणाम और व्याख्या", "Correct!": "सही!", "Incorrect": "गलत", "Unanswered": "उत्तर नहीं दिया", "Explanation:": "व्याख्या:",
        "Diabetes Awareness & Glucose Management": "मधुमेह जागरूकता और ग्लूकोज़ प्रबंधन",
        "Heart Health & Hypertension Awareness": "हृदय स्वास्थ्य और उच्च रक्तचाप जागरूकता",
        "Vaccination Concepts & Adult Immunization": "टीकाकरण अवधारणाएं और वयस्क टीकाकरण",
        "Seasonal Respiratory Illness & Prevention": "मौसमी श्वसन बीमारी और रोकथाम",
    },
    "ta": {
        "Language": "மொழி", "App": "செயலி", "Consultations": "ஆலோசனைகள்",
        "New Consultation": "புதிய ஆலோசனை", "Select Consultation": "ஆலோசனையைத் தேர்ந்தெடுக்கவும்",
        "Educational Notice": "கல்வித் தகவல்", "Home": "முகப்பு", "AI Healthcare Chat": "AI சுகாதார உரையாடல்",
        "Health Learning": "சுகாதாரக் கற்றல்", "Interactive Quizzes": "வினாடி வினாக்கள்",
        "Risk Assessment": "ஆபத்து மதிப்பீடு", "Myth vs Fact": "கட்டுக்கதை vs உண்மை",
        "Symptom Checker": "அறிகுறி சரிபார்ப்பு", "Medications": "மருந்துகள்", "Appointments": "சந்திப்புகள்",
        "Healthcare Directory": "சுகாதார அடைவு", "Insurance & Billing": "காப்பீடு மற்றும் பில்லிங்",
        "Mental Wellness": "மனநலம்", "Wearable Health": "அணியக்கூடிய சுகாதாரம்",
        "Profile": "சுயவிவரம்", "Settings": "அமைப்புகள்",
        "Quick Topics — click to ask:": "விரைவு தலைப்புகள் — கேட்க கிளிக் செய்யவும்:",
        "Voice / Audio Input": "குரல் / ஆடியோ உள்ளீடு",
        "Say hello or ask a health question": "வணக்கம் சொல்லுங்கள் அல்லது சுகாதாரக் கேள்வி கேளுங்கள்",
        "Health Learning Curriculum": "சுகாதாரக் கற்றல் பாடத்திட்டம்",
        "Evidence-grounded, bite-sized lessons to enhance your healthcare literacy and preventive habits.": "உங்கள் சுகாதார அறிவையும் தடுப்பு பழக்கங்களையும் மேம்படுத்தும் ஆதார அடிப்படையிலான சிறு பாடங்கள்.",
        "Category": "வகை", "Estimated reading time": "மதிப்பிடப்பட்ட வாசிப்பு நேரம்", "Lessons": "பாடங்கள்", "Lesson": "பாடம்", "Key Takeaways": "முக்கிய குறிப்புகள்",
        "Mark": "குறிக்கவும்", "Completed": "முடிந்தது", "You have completed this educational module!": "இந்த கல்வி தொகுதியை முடித்துவிட்டீர்கள்!",
        "Healthcare education does not substitute for personalized medical check-ups with your physician.": "சுகாதாரக் கல்வி உங்கள் மருத்துவரின் தனிப்பட்ட மருத்துவ பரிசோதனைகளுக்கு மாற்றாகாது.",
        "Interactive Healthcare Quizzes": "ஊடாடும் சுகாதார வினாடி வினாக்கள்", "Choose Quiz Topic:": "வினாடி வினா தலைப்பைத் தேர்ந்தெடுக்கவும்:", "Restart / Load New Questions": "மீண்டும் தொடங்கு / புதிய கேள்விகளை ஏற்று", "Submit Quiz Answers": "வினாடி வினா பதில்களைச் சமர்ப்பிக்கவும்", "Question": "கேள்வி", "Select your answer for question": "கேள்விக்கான பதிலைத் தேர்ந்தெடுக்கவும்", "Quiz Results & Explanations": "வினாடி வினா முடிவுகள் மற்றும் விளக்கங்கள்", "Correct!": "சரி!", "Incorrect": "தவறு", "Unanswered": "பதில் இல்லை", "Explanation:": "விளக்கம்:",
        "Diabetes Awareness & Glucose Management": "நீரிழிவு விழிப்புணர்வு மற்றும் குளுக்கோஸ் மேலாண்மை",
        "Heart Health & Hypertension Awareness": "இதய ஆரோக்கியம் மற்றும் உயர் இரத்த அழுத்த விழிப்புணர்வு",
        "Vaccination Concepts & Adult Immunization": "தடுப்பூசி கருத்துகள் மற்றும் பெரியோர் தடுப்பூசி",
        "Seasonal Respiratory Illness & Prevention": "பருவகால சுவாச நோய் மற்றும் தடுப்பு",
    },
    "kn": {
        "Language": "ಭಾಷೆ", "App": "ಆ್ಯಪ್", "Consultations": "ಸಮಾಲೋಚನೆಗಳು",
        "New Consultation": "ಹೊಸ ಸಮಾಲೋಚನೆ", "Select Consultation": "ಸಮಾಲೋಚನೆ ಆಯ್ಕೆಮಾಡಿ",
        "Educational Notice": "ಶೈಕ್ಷಣಿಕ ಮಾಹಿತಿ", "Home": "ಮುಖಪುಟ", "AI Healthcare Chat": "AI ಆರೋಗ್ಯ ಚಾಟ್",
        "Health Learning": "ಆರೋಗ್ಯ ಕಲಿಕೆ", "Interactive Quizzes": "ಸಂವಾದಾತ್ಮಕ ಕ್ವಿಜ್‌ಗಳು",
        "Risk Assessment": "ಅಪಾಯ ಮೌಲ್ಯಮಾಪನ", "Myth vs Fact": "ಮಿಥ್ಯೆ vs ಸತ್ಯ",
        "Symptom Checker": "ಲಕ್ಷಣ ಪರಿಶೀಲನೆ", "Medications": "ಔಷಧಗಳು", "Appointments": "ಅಪಾಯಿಂಟ್‌ಮೆಂಟ್‌ಗಳು",
        "Healthcare Directory": "ಆರೋಗ್ಯ ಡೈರೆಕ್ಟರಿ", "Insurance & Billing": "ವಿಮೆ ಮತ್ತು ಬಿಲ್ಲಿಂಗ್",
        "Mental Wellness": "ಮಾನಸಿಕ ಸ್ವಾಸ್ಥ್ಯ", "Wearable Health": "ಧರಿಸಬಹುದಾದ ಆರೋಗ್ಯ",
        "Profile": "ಪ್ರೊಫೈಲ್", "Settings": "ಸೆಟ್ಟಿಂಗ್‌ಗಳು",
        "Quick Topics — click to ask:": "ತ್ವರಿತ ವಿಷಯಗಳು — ಕೇಳಲು ಕ್ಲಿಕ್ ಮಾಡಿ:",
        "Voice / Audio Input": "ಧ್ವನಿ / ಆಡಿಯೋ ಇನ್‌ಪುಟ್",
        "Say hello or ask a health question": "ಹಲೋ ಹೇಳಿ ಅಥವಾ ಆರೋಗ್ಯ ಪ್ರಶ್ನೆ ಕೇಳಿ",
        "Health Learning Curriculum": "ಆರೋಗ್ಯ ಕಲಿಕಾ ಪಠ್ಯಕ್ರಮ",
        "Evidence-grounded, bite-sized lessons to enhance your healthcare literacy and preventive habits.": "ನಿಮ್ಮ ಆರೋಗ್ಯ ಜ್ಞಾನ ಮತ್ತು ತಡೆಗಟ್ಟುವ ಅಭ್ಯಾಸಗಳನ್ನು ಹೆಚ್ಚಿಸುವ ಸಾಕ್ಷ್ಯಾಧಾರಿತ ಸಣ್ಣ ಪಾಠಗಳು.",
        "Category": "ವರ್ಗ", "Estimated reading time": "ಅಂದಾಜು ಓದುವ ಸಮಯ", "Lessons": "ಪಾಠಗಳು", "Lesson": "ಪಾಠ", "Key Takeaways": "ಮುಖ್ಯ ಅಂಶಗಳು",
        "Mark": "ಗುರುತಿಸಿ", "Completed": "ಪೂರ್ಣಗೊಂಡಿದೆ", "You have completed this educational module!": "ನೀವು ಈ ಶೈಕ್ಷಣಿಕ ಮಾಡ್ಯೂಲ್ ಅನ್ನು ಪೂರ್ಣಗೊಳಿಸಿದ್ದೀರಿ!",
        "Healthcare education does not substitute for personalized medical check-ups with your physician.": "ಆರೋಗ್ಯ ಶಿಕ್ಷಣವು ನಿಮ್ಮ ವೈದ್ಯರ ವೈಯಕ್ತಿಕ ವೈದ್ಯಕೀಯ ತಪಾಸಣೆಗೆ ಪರ್ಯಾಯವಲ್ಲ.",
        "Interactive Healthcare Quizzes": "ಸಂವಾದಾತ್ಮಕ ಆರೋಗ್ಯ ಕ್ವಿಜ್‌ಗಳು", "Choose Quiz Topic:": "ಕ್ವಿಜ್ ವಿಷಯವನ್ನು ಆಯ್ಕೆಮಾಡಿ:", "Restart / Load New Questions": "ಮತ್ತೆ ಪ್ರಾರಂಭಿಸಿ / ಹೊಸ ಪ್ರಶ್ನೆಗಳನ್ನು ಲೋಡ್ ಮಾಡಿ", "Submit Quiz Answers": "ಕ್ವಿಜ್ ಉತ್ತರಗಳನ್ನು ಸಲ್ಲಿಸಿ", "Question": "ಪ್ರಶ್ನೆ", "Select your answer for question": "ಪ್ರಶ್ನೆಗೆ ನಿಮ್ಮ ಉತ್ತರವನ್ನು ಆಯ್ಕೆಮಾಡಿ", "Quiz Results & Explanations": "ಕ್ವಿಜ್ ಫಲಿತಾಂಶಗಳು ಮತ್ತು ವಿವರಣೆಗಳು", "Correct!": "ಸರಿಯಾಗಿದೆ!", "Incorrect": "ತಪ್ಪು", "Unanswered": "ಉತ್ತರಿಸಲಾಗಿಲ್ಲ", "Explanation:": "ವಿವರಣೆ:",
        "Diabetes Awareness & Glucose Management": "ಮಧುಮೇಹ ಜಾಗೃತಿ ಮತ್ತು ಗ್ಲೂಕೋಸ್ ನಿರ್ವಹಣೆ",
        "Heart Health & Hypertension Awareness": "ಹೃದಯ ಆರೋಗ್ಯ ಮತ್ತು ಅಧಿಕ ರಕ್ತದೊತ್ತಡ ಜಾಗೃತಿ",
        "Vaccination Concepts & Adult Immunization": "ಲಸಿಕೆ ಪರಿಕಲ್ಪನೆಗಳು ಮತ್ತು ವಯಸ್ಕರ ಲಸಿಕೆ",
        "Seasonal Respiratory Illness & Prevention": "ಋತುಮಾನಿಕ ಉಸಿರಾಟದ ಕಾಯಿಲೆ ಮತ್ತು ತಡೆಗಟ್ಟುವಿಕೆ",
    },
}


def translate_ui(text: str, language: str = "en") -> str:
    """Translate approved shared UI labels without translating medical facts."""
    return UI_TRANSLATIONS.get(language, {}).get(text, text)


def localize_response(response: str, language: str = "en") -> str:
    """Translate response structure and verified dataset prevention facts offline."""
    labels = LABELS.get(language)
    if not labels:
        return response
    replacements = {
        "## Verified Health Awareness Information": labels["facts_heading"],
        "The following points come directly from the most relevant verified health source:": labels["facts_intro"],
        "## How can it be prevented or reduced?": labels["prevention_heading"],
        "### How can it be prevented or reduced?": labels["prevention_heading"].replace("## ", "### ", 1),
        "**Educational Notice:** This information is for general health awareness only. It is not a diagnosis or personalized medical advice. Consult a qualified healthcare professional.": labels["notice"],
        "Disease:": f"{labels['disease']}:", "Category:": f"{labels['category']}:", "Cause:": f"{labels['cause']}:",
        "Transmission:": f"{labels['transmission']}:", "Common symptoms:": f"{labels['symptoms']}:",
        "Prevention:": f"{labels['prevention']}:", "Medical note:": f"{labels['medical_note']}:",
    }
    for source, translated in replacements.items():
        response = response.replace(source, translated)
    for source, translated in FIELD_TRANSLATIONS.get(language, {}).items():
        response = response.replace(source, translated)
    return response


def localize_greeting(language: str = "en") -> str:
    return LABELS.get(language, {}).get("greeting", "Hi! I'm HealthAware AI. I'm doing well, thank you. How can I help you today? You can ask me about symptoms, prevention, nutrition, medications, or general wellness.")
