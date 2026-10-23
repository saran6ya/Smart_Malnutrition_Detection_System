# PRJ_493 Smart Malnutrition Detection System
## Nutrition Awareness Knowledge Base for RAG

**Version:** 1.0  
**Purpose:** Structured source for the Streamlit Nutrition Awareness page.  
**Safety:** Academic prototype only; not a diagnostic or treatment system.

## Retrieval map
- `Healthy` → `HEALTHY_001`, `HEALTHY_002`, `HEALTHY_003`, plus `GENERAL_001`.
- `Malnourished` → `MALNUTRITION_001`, `MALNUTRITION_002`, `MALNUTRITION_003`, plus `GENERAL_001`.
- `No objects detected`, `Unknown`, or unsupported class → `NO_DETECTION_001` plus `GENERAL_001`.
- Use the exact model label; never infer a class when no supported prediction exists.

## Safety rules
- A model label is not a medical diagnosis.
- Do not provide personalised diet plans, calorie targets, supplement doses, or treatment.
- Recommend a qualified healthcare professional for nutrition concerns.
- Preserve the disclaimer in the UI.

## GENERAL_001 — Purpose, scope, and safety

**Category:** `general_safety`  
**Audience:** `all`  
**Trigger labels:** Healthy, Malnourished, No objects detected, Unknown

This knowledge base provides general nutrition education for the PRJ_493 Smart Malnutrition Detection System. It supports an educational Streamlit demonstration by retrieving relevant passages after an image model returns a class label.

A YOLO image prediction is not a medical diagnosis and cannot establish a person's nutritional status. A model may be wrong, uncertain, and unsuitable for some real-world conditions. The app must describe its result as an AI-generated image prediction, not a confirmed health condition.

Nutrition information here is general. Individual needs depend on age, growth, pregnancy or breastfeeding, activity, culture, food availability, allergies, medical conditions, and other factors. The app must not generate personalised calorie targets, treatment plans, supplement doses, or claims that a food will cure malnutrition.

For concerns about a child's growth, persistent poor appetite, unexplained weight loss, or weakness, encourage assessment by a qualified healthcare professional or registered dietitian. Severe or rapidly worsening symptoms require prompt medical care.

## HEALTHY_001 — Healthy prediction: balanced eating

**Category:** `healthy_awareness`  
**Audience:** `all`  
**Trigger labels:** Healthy

When the model output is Healthy, display this as general maintenance education—not proof that the person is healthy. A balanced eating pattern includes variety, adequacy, balance, moderation, and food safety. Combine foods from different food groups according to individual needs, cultural preferences, and local availability.

Examples include staple grains such as rice, wheat, millet, oats, or other whole grains; pulses such as lentils, dal, beans, and chickpeas; vegetables; fruits; and protein foods such as eggs, milk, curd, fish, meat, soy foods, nuts, and seeds where suitable. No single food provides every nutrient.

Encourage varied meals with a mix of food groups where possible. Do not present a single fixed diet as suitable for everyone. Appropriate balance and portions differ between individuals.

## HEALTHY_002 — Healthy prediction: protein and varied foods

**Category:** `healthy_awareness`  
**Audience:** `all`  
**Trigger labels:** Healthy

Protein contributes to the growth and maintenance of body tissues. Common sources include dal, lentils, chickpeas, beans, soy foods, milk, curd, eggs, fish, and lean meat. Choices should fit preferences, culture, budget, allergies, and medical needs.

A varied diet also supplies carbohydrates for energy, fats, vitamins, minerals, and dietary fibre. Whole grains, pulses, vegetables, fruits, nuts, and seeds contribute to dietary variety. Do not advise excessive protein or supplements based only on an image prediction. People with kidney disease or other medical conditions may need individual advice from a healthcare professional.

## HEALTHY_003 — Healthy prediction: fruits, vegetables, hydration, and food safety

**Category:** `healthy_awareness`  
**Audience:** `all`  
**Trigger labels:** Healthy

A variety of seasonal fruits and vegetables can contribute vitamins, minerals, and fibre. Fresh, frozen, or appropriately preserved options may be useful depending on access and availability. Choose safe drinking water and handle, store, and prepare food hygienically.

Fluid needs vary with age, climate, activity, pregnancy or breastfeeding, and health conditions. Encourage regular access to safe water without giving a universal volume target to every user. A healthy dietary pattern generally limits excessive salt, free sugars, and unhealthy fats while prioritising a variety of minimally processed foods.

## MALNUTRITION_001 — Malnutrition prediction: what the term means

**Category:** `malnutrition_awareness`  
**Audience:** `all`  
**Trigger labels:** Malnourished

The model's label Malnourished is an AI-generated prediction, not a diagnosis. Malnutrition is a broad term that can include deficiencies, excesses, or imbalances in energy and/or nutrients. Undernutrition can include wasting, stunting, underweight, and micronutrient deficiencies. Malnutrition also includes overweight, obesity, and some diet-related health conditions.

A single image cannot reliably determine a person's nutritional status. Clinical assessment may require age, growth history, weight and height measurements, dietary history, symptoms, examination, and tests when appropriate. Do not infer a diagnosis, severity, cause, or treatment from the model output alone.

## MALNUTRITION_002 — Malnutrition prediction: supportive food education

**Category:** `malnutrition_awareness`  
**Audience:** `all`  
**Trigger labels:** Malnourished

If the model predicts Malnourished, provide supportive, non-judgmental information and recommend professional assessment. A varied diet may include energy-providing staple foods, protein sources, vegetables, fruits, and sources of fats, depending on the person's needs and available foods.

Examples of protein-containing foods include dal, beans, chickpeas, lentils, soy foods, milk, curd, eggs, fish, and meat where appropriate. Nuts, seeds, and suitable oils can contribute energy and fats. These are examples, not a prescribed recovery diet. Food texture, portion sizes, meal frequency, energy needs, allergies, age, and medical conditions may require professional guidance.

Do not prescribe high-calorie diets, supplements, therapeutic foods, or micronutrient doses through this app. Do not suggest that a particular food will cure malnutrition.

## MALNUTRITION_003 — Malnutrition prediction: when to seek professional support

**Category:** `malnutrition_awareness`  
**Audience:** `all`  
**Trigger labels:** Malnourished

Encourage users to consult a qualified healthcare professional or registered dietitian if they are concerned about unexplained weight loss, persistent poor appetite, ongoing weakness, feeding difficulties, or a child's growth. Children should be assessed by a qualified professional when growth or nutrition is a concern; their needs differ from adults.

Seek urgent medical care for severe or rapidly worsening symptoms, inability to keep fluids down, fainting, confusion, or other emergency warning signs. The app must not delay care or imply that a model result can replace a clinical assessment. Use respectful language and avoid blame or stigma.

## NO_DETECTION_001 — No detection or unsupported result

**Category:** `fallback`  
**Audience:** `all`  
**Trigger labels:** No objects detected, Unknown, Other

If the model returns No objects detected, Unknown, or another unsupported label, do not assume the person is Healthy or Malnourished. Explain that the model did not produce a supported result. The user may try a clear image if appropriate, but the app should not promise that a new image will provide a reliable health assessment.

Show general nutrition education only if clearly labelled as general information, and recommend professional support for health concerns. Never map every unexpected class to Malnourished or Healthy by default.

## RAG_001 — Retrieval and display rules

**Category:** `retrieval_instructions`  
**Audience:** `application`  
**Trigger labels:** Healthy, Malnourished, No objects detected, Unknown

Use the exact class name returned by YOLO to select relevant knowledge chunks. For Healthy, retrieve HEALTHY_001, HEALTHY_002, and HEALTHY_003 plus GENERAL_001. For Malnourished, retrieve MALNUTRITION_001, MALNUTRITION_002, and MALNUTRITION_003 plus GENERAL_001. For No objects detected, Unknown, or an unrecognised label, retrieve NO_DETECTION_001 and GENERAL_001.

The class label is a retrieval filter, not a medical fact. Return only relevant passages from this knowledge base and preserve the disclaimer. If no relevant chunks are found, display a safe fallback rather than inventing advice. Display source titles and references when available. Do not claim that retrieved information is a personalised treatment plan.

## SOURCE_001 — Source notes and further reading

**Category:** `references`  
**Audience:** `application`  
**Trigger labels:** all

This educational overview is informed by public health resources. They provide general principles; they do not validate the PRJ_493 model or its predictions.

1. World Health Organization (WHO), “Malnutrition,” fact sheet, 1 March 2024: https://www.who.int/en/news-room/fact-sheets/detail/malnutrition
2. World Health Organization (WHO), “Malnutrition,” questions and answers, 7 May 2025: https://www.who.int/news-room/questions-and-answers/item/malnutrition
3. World Health Organization (WHO), “Healthy diet,” fact sheet, 26 January 2026: https://www.who.int/news-room/fact-sheets/detail/healthy-diet
4. WHO and Food and Agriculture Organization of the United Nations (FAO), “What are healthy diets? Joint statement,” 2024: https://www.who.int/publications/i/item/9789240101876

Review the linked resources for updates before deployment. Obtain appropriate clinical review if the app is intended for use beyond an academic demonstration.
