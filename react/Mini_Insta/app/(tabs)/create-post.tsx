import { useState } from 'react';
import { Alert, Pressable, ScrollView, Text, TextInput, View } from 'react-native';
import styles from '../../assets/my_styles';
import { useAuth } from '@/context/AuthContext';

const thisProfile = 1;
const API_BASE_URL = 'https://cs-webapps.bu.edu/ksolter/mini_insta/api';

type CreatedPost = {
  id: number;
  caption: string;
};

export default function CreatePost() {
  const { token } = useAuth();

  const getAuthHeaders = (): Record<string, string> => {
    if (!token) {
      return {};
    }

    return {
      Authorization: `Token ${token}`,
    };
  };

  const [caption, setCaption] = useState('');
  const [imageUrl, setImageUrl] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const createPost = async () => {
    if (!caption.trim()) {
      Alert.alert('Missing caption', 'Please enter a caption before submitting.');
      return;
    }

    try {
      setIsSubmitting(true);

      const postResponse = await fetch(`${API_BASE_URL}/profiles/${thisProfile}/posts/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...getAuthHeaders(),
        },
        body: JSON.stringify({
          caption: caption.trim(),
        }),
      });

      if (!postResponse.ok) {
        throw new Error('Could not create post.');
      }

      const createdPost: CreatedPost = await postResponse.json();

      if (imageUrl.trim()) {
        const photoResponse = await fetch(`${API_BASE_URL}/photos/create/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            ...getAuthHeaders(),
          },
          body: JSON.stringify({
            post: createdPost.id,
            image_url: imageUrl.trim(),
          }),
        });

        if (!photoResponse.ok) {
          throw new Error('Post was created, but image URL could not be attached.');
        }
      }

      setCaption('');
      setImageUrl('');
      Alert.alert('Success', 'Post created successfully.');
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Something went wrong.';
      Alert.alert('Error', message);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <ScrollView>
      <View style={styles.mediumContainer}>
        <View style={styles.titleContainer}>
          <Text style={styles.titleText}>Create Post</Text>
        </View>

        <View style={styles.smallContainer}>
          <Text style={styles.paragraphText}>Caption</Text>
          <View style={styles.inputboxcontainer}>
            <TextInput
              value={caption}
              onChangeText={setCaption}
              placeholder="Write something..."
              style={styles.inputbox}
            />
          </View>

          <Text style={styles.paragraphText}>Image URL (optional)</Text>
          <View style={styles.inputboxcontainer}>
            <TextInput
              value={imageUrl}
              onChangeText={setImageUrl}
              placeholder="https://..."
              autoCapitalize="none"
              style={styles.inputbox}
            />
          </View>

          <Pressable
            onPress={createPost}
            style={({ pressed }) => [
              styles.submitButton,
              pressed ? styles.submitButtonPressed : null,
            ]}
            disabled={isSubmitting}
          >
            <Text style={styles.submitButtonText}>
              {isSubmitting ? 'Submitting...' : 'Create Post'}
            </Text>
          </Pressable>
        </View>
      </View>
    </ScrollView>
  );
}
