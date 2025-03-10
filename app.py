import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import preprocessor, helper
import seaborn as sns

st.sidebar.title('WhatsApp Chat Analyzer')

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    try :
        bytes_data = uploaded_file.getvalue()
        data = bytes_data.decode("utf-8")
        df = preprocessor.preprocess(data)
            
        # Fetch unique users
        user_list = df['user'].unique().tolist()
        user_list.remove('group_notification')
        user_list.sort()
        user_list.insert(0, "Overall")
        selected_user = st.sidebar.selectbox('Show analysis wrt', user_list)
        
        if st.sidebar.button("Show Analysis"):
            
            # Stats Area
            num_messages, words, num_media_message, num_links = helper.fetch_stats(selected_user, df)

            st.title("Top Statistics")
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric(label="Total Messages", value=num_messages)
            with col2:
                st.metric(label="Total Words", value=words)
            with col3:
                st.metric(label="Media Messages", value=num_media_message)
            with col4:
                st.metric(label="Number of Links", value=num_links)
                
                
            #monthly timeline analysis
            st.title("Monthly Timeline Analysis")
            timeline =helper.monthly_timeline(selected_user,df)
            fig,ax=plt.subplots()
            ax.plot(timeline['time'],timeline['message'],color='violet')
            plt.xticks(rotation = 'vertical')
            st.pyplot(fig)
            
            #Daily timeline analysis
            st.title("Daily Timeline Analysis")
            daily_timeline =helper.daily_timeline(selected_user,df)
            fig,ax=plt.subplots()
            ax.plot(daily_timeline['only_date'],daily_timeline['message'],color='orange')
            plt.xticks(rotation = 'vertical')
            st.pyplot(fig)
            
            # activity map:-
            st.title("Weekly Activity Map")
            col1,col2 = st.columns(2)
            
            with col1:
                st.header("Most Active Days")
                most_active_days =helper.week_activity_map(selected_user,df)
                
                fig,ax = plt.subplots()
                ax.bar(most_active_days.index,most_active_days.values,color='gold')
                plt.xticks(rotation = 'vertical')
                st.pyplot(fig)
            with col2:
                st.header("Most Active Months")
                most_active_months =helper.month_activity_map(selected_user,df)
                
                fig,ax = plt.subplots()
                ax.bar(most_active_months.index,most_active_months.values,color='tomato')
                plt.xticks(rotation = 'vertical')
                st.pyplot(fig) 
                
            # headmap
            st.title("Activity Heatmap")
            user_heatmap =helper.activity_heatmap(selected_user,df)
            fig,ax = plt.subplots()
            ax=sns.heatmap(user_heatmap)
            st.pyplot(fig)  
                
            
            # Finding the most active user (group level)
            if selected_user == 'Overall':
                st.title("Most Active User")
                x, new_df = helper.most_active_user(df)
                fig, ax = plt.subplots()
                col1, col2 = st.columns(2)
                
                with col1:
                    ax.bar(x.index, x.values, color="cyan")
                    plt.xticks(rotation='vertical')
                    st.pyplot(fig)
                with col2:
                    st.dataframe(new_df)
            
            # Word Cloud
            st.title("Word Cloud")
            df_wc = helper.create_word_cloud(selected_user, df)
            fig, ax = plt.subplots()
            ax.imshow(df_wc)
            st.pyplot(fig)
            
            #Most comman words:-
            most_common_df=helper.most_common_words(selected_user,df)
            st.title("Most Common Words")
            fig,ax=plt.subplots()
            ax.barh(most_common_df[0],most_common_df[1],color='green')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
            
            # emoji analysis
            emoji_df = helper.emoji_helper(selected_user,df)
            st.title("Emoji Analysis")

            col1,col2 = st.columns(2)

            with col1:
                st.dataframe(emoji_df)
            with col2:
                plt.rcParams['font.family'] = 'Segoe UI Emoji' 
                fig,ax = plt.subplots()
                ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(),autopct="%0.2f")
                st.pyplot(fig)   
            
        
    except Exception as e:
        st.write(f"Error: The uploaded document is not supported or is corrupted. \n Use another file...")    
       
        
        














