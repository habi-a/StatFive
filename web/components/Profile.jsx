import React from "react";
// Chakra imports
import { Flex, Image, Text, useColorModeValue } from "@chakra-ui/react";

function Profile(data) {
  let boxBg = useColorModeValue("white !important", "#111c44 !important");
  let mainText = useColorModeValue("gray.800", "white");
  let secondaryText = useColorModeValue("gray.400", "gray.400");

  return (
    <Flex
      borderRadius='20px'
      bg={boxBg}
      p='20px'
      w={{ base: "315px", md: "345px" }}
      alignItems='center'
      margin="20px auto"
      direction='column'>
      <Flex flexDirection='column' mb='30px'>
        <Text
          fontWeight='600'
          color={mainText}
          textAlign='center'
          fontSize='xl'>
          {data?.data?.lastname} {data?.data?.firstname}
        </Text>
        <Text
          color={secondaryText}
          textAlign='center'
          fontSize='sm'
          fontWeight='500'>
          Mon poste : {data?.data?.post}
        </Text>
      </Flex>
      <Flex justify='space-between' w='100%' px='36px'>
        <Text><Text fontWeight="bold">Description :</Text> {data?.data?.description}</Text>
      </Flex>
    </Flex>
  );
}

export default Profile;