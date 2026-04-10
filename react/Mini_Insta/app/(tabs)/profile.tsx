import { Text, View, Image } from 'react-native';
import styles from '../../assets/my_styles';
import { useState, useEffect } from 'react';

const thisProfile = 1;
const SITE_BASE_URL = 'https://cs-webapps.bu.edu';
const API_BASE_URL = 'https://cs-webapps.bu.edu/ksolter/mini_insta/api';

type Profile = {
  id: number;
  join_date: string;
  username: string;
  display_name: string;
  profile_image_url?: string | null;
  bio_text?: string;
  user: number;
};

const resolveImageUri = (imageUrl?: string | null): string | null => {
  if (!imageUrl) {
    return null;
  }

  if (imageUrl.startsWith('http://') || imageUrl.startsWith('https://')) {
    return imageUrl;
  }

  if (imageUrl.startsWith('/')) {
    return `${SITE_BASE_URL}${imageUrl}`;
  }

  return `${SITE_BASE_URL}/${imageUrl}`;
};

export default function Profile() {

  const [profile, setProfile] = useState<Profile | null>(null);

  const fetchProfile = async (url: string) =>{
    const response = await fetch(url);
    const data = await response.json();
    setProfile(data);
  };

  useEffect(() => {
    fetchProfile(`${API_BASE_URL}/profiles/${thisProfile}/`);
  }, []);

  const profileImageUri = resolveImageUri(profile?.profile_image_url);
  const joinedLabel = profile?.join_date
    ? new Date(profile.join_date).toLocaleDateString()
    : '';

  return (
    <View style={styles.mediumContainer}>
      <View style={styles.titleContainer}>
        <Text style={styles.titleText}>Profile</Text>
      </View>
        <View style={styles.mediumContainer}>
          {!profile ? (
            <Text style={styles.paragraphText}>Loading profile...</Text>
          ) : (
            <View style={styles.mediumContainer}>
              {profileImageUri ? (
                <Image
                  source={{ uri: profileImageUri }}
                  style={styles.image}
                  resizeMode="cover"
                />
              ) : (
                <Text style={styles.paragraphText}>No profile image available.</Text>
              )}

              <Text style={styles.paragraphText}>Display Name: {profile.display_name}</Text>
              <Text style={styles.paragraphText}>Username: {profile.username}</Text>
              <Text style={styles.paragraphText}>Bio: {profile.bio_text || 'No bio yet.'}</Text>
              <Text style={styles.paragraphText}>Joined: {joinedLabel}</Text>
            </View>
          )}
        </View>
    </View>
  );
};
