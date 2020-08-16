import React, { useState, useLayoutEffect } from 'react';

import {
  View,
  Text,
  TextInput,
  Button,
  Image,
  TouchableNativeFeedback,
} from 'react-native';
import HeaderButton from '../components/HeaderButton';
import Filter from '../components/Filter';
import DeviceComp from '../components/DeviceComp';

const SettingsPage = ({ navigation }) => {
  useLayoutEffect(() => {
    navigation.setOptions({
      headerLeft: () => {
        return (
          <HeaderButton
            name="ios-arrow-round-back"
            color="white"
            size={38}
            onPress={() => {
              navigation.goBack();
            }}
          />
        );
      },
    });
  });
  const [notify, setNotify] = useState(false);
  const [vibrate, setVibrate] = useState(false);
  return (
    <View style={{ flex: 1, alignItems: 'center' }}>
      <View style={{ width: '100%', height: 290 }}>
        <Image
          style={{ width: '100%', height: '100%' }}
          source={{
            uri:
              'https://cdn.shopify.com/s/files/1/2382/6729/products/SP125306.jpg?v=1585341802',
          }}
        />
      </View>
      <TextInput
        style={{
          width: '80%',
          borderBottomWidth: 1,
          borderBottomColor: 'grey',
          padding: 5,
          marginVertical: 12,
          //   alignSelf: 'flex-start',
        }}
        placeholder="Set limit"
      />
      <Button title="Set Limit" />
      <Filter
        name="Notify when limit exceeds"
        toggleSwitch={() => setNotify((pre) => !pre)}
        state={notify}
      />
      <Filter
        name="Vibrate when people are close"
        toggleSwitch={() => setVibrate((pre) => !pre)}
        state={vibrate}
      />
      <Text
        style={{
          fontWeight: 'bold',
          fontSize: 18,
          color: 'black',
          borderWidth: 1,
          borderColor: 'grey',
          paddingHorizontal: 12,
          paddingVertical: 5,
          marginVertical: 12,
        }}
      >
        You interacted with 2 people, today
      </Text>
      <DeviceComp name="SOURAV07" />
      <DeviceComp name="DEBRUP28" />
    </View>
  );
};

export default SettingsPage;
