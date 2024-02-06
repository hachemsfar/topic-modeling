from django.shortcuts import render
from django.http import HttpResponse
from .models import TopicInfo
from .modelIntegration import predict_topic
from django.shortcuts import redirect
import os

def home(request):
    if request.method == 'POST':
        text_area = request.POST['text_area']
        new_topics, new_probs, topic_info = predict_topic(text_area)
        selected_data=topic_info[topic_info['Topic']==new_topics[0]][['Topic','Name','CustomName','Representation','KeyBERT','Llama2','MMR']]
        # Save data to PostgreSQL after form validation
        if new_topics:
            try:
                Topic=TopicInfo(
                    Topic=selected_data['Topic'].iloc[0],
                    Text=str(text_area),
                    Name=selected_data['Name'].iloc[0],
                    Custom_Name=selected_data['CustomName'].iloc[0],
                    Representation=selected_data['Representation'].iloc[0],
                    keyBert=selected_data['KeyBERT'].iloc[0],
                    Llama2=selected_data['Llama2'].iloc[0],
                    MMR=selected_data['MMR'].iloc[0],
                )
                Topic.save()
            except Exception as e:
                # Handle any exceptions, e.g., database errors
                return HttpResponse(f"Error: {e}")
            
            # Redirect after successful form submission
            return render(request, 'home.html', {'new_topics': new_topics[0], 'new_probs': new_probs[0], 'selected_data': selected_data.iloc[0].to_dict()})

    return render(request, 'home.html')