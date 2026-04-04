// react/DadJoke/assets/my_styles.ts 
// Author: Kai Solter
// This is a stylesheet for the app, defining common styles for text and images
import { StyleSheet } from 'react-native';

const styles = StyleSheet.create({
    mediumContainer: {
        width: '80%',
        alignSelf: 'center',
        alignItems: 'center',
        justifyContent: 'center',
        backgroundColor: 'lightgray',
        paddingVertical: 16,
    },
    smallContainer: {
        width: '80%',
        alignSelf: 'center',
        alignItems: 'center',
        justifyContent: 'center',
        backgroundColor: '#d2f4f3',
        paddingVertical: 16,
        paddingHorizontal: 8,
        marginBottom: 16,
    },

    inputboxcontainer: {
        flexDirection: 'row',
        alignItems: 'center',
        justifyContent: 'center',
        borderWidth: 1,
        borderColor: 'gray',
        backgroundColor: 'white',
    },

    inputbox: {
        fontSize: 16,
        color : 'black',
    },
  
    textContainer: {
        alignItems: 'center',
    },

    titleContainer: {
        alignItems: 'center',
        marginBottom: 16,
        borderWidth: 1,
        borderColor: 'gray',
        backgroundColor: 'darkgray',
        padding: 8,
    },
    
    titleText: {
        fontSize: 20,
        fontWeight: 'bold',
        color : 'black',
    },
    subTitleText: {
        fontSize: 16,
        color : 'black',
    },
    paragraphText: {
        fontSize: 14,
        color : 'black',
    },
    image: {
        width: 180,
        height: 180,
    },
    wideImage: {
        width: 300,
        height: 200,
    },
    submitButton: {
        backgroundColor: '#3b82f6',
        paddingVertical: 10,
        paddingHorizontal: 16,
        borderRadius: 8,
    },
    submitButtonPressed: {
        backgroundColor: '#1d4ed8',
    },
    submitButtonText: {
        color: 'white',
        fontWeight: '600',
    },
});

export default styles;