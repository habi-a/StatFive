import {
    IconButton,
    Box,
    CloseButton,
    Flex,
    Icon,
    useColorModeValue,
    Link,
    Drawer,
    DrawerContent,
    Text,
    useDisclosure,
    Image
  } from '@chakra-ui/react';
  import {
    FiHome,
    FiCompass,
    FiSettings,
    FiMenu,
  } from 'react-icons/fi';
  import {
    RiProfileLine,
    RiFolderHistoryLine,
    RiFootballFill,
    RiAdminLine
  } from 'react-icons/ri'
  import {
    MdAdminPanelSettings
  } from 'react-icons/md'
import {useStore} from "../pages/index"
import { useState, useEffect } from 'react';
import { getMe } from "@mokhta_s/react-statfive-api";

  export default function SimpleSidebar({ children }) {
    const { isOpen, onOpen, onClose } = useDisclosure();

    return (
      <Box>
        <SidebarContent
          onClose={() => onClose}
          display={{ base: 'none', md: 'block' }}
        />
        <Drawer
          autoFocus={false}
          isOpen={isOpen}
          placement="left"
          onClose={onClose}
          returnFocusOnClose={false}
          onOverlayClick={onClose}
          size="full">
          <DrawerContent>
            <SidebarContent onClose={onClose} />
          </DrawerContent>
        </Drawer>
        {/* mobilenav */}
        <MobileNav display={{ base: 'flex', md: 'none' }} onOpen={onOpen} />
        <Box ml={{ base: 0, md: 60 }} p="4">
          {children}
        </Box>
      </Box>
    );
  }
  
  const SidebarContent = ({ onClose, ...rest }) => {
    const [user, setUser] = useState(null)
    const data = useStore((state) => state.data)

    const getUser = async () => {
      const result = await getMe();
      if (!result?.data.error) {
        setUser(result.data.data);
      }
    };

    useEffect(() => {
      getUser()
    }, [])

    const LinkItems = [
      { name: 'Accueil', href: "/accueil", icon: FiHome },
      { name: 'Mon profil', href: "/profil", icon: RiProfileLine },
      { name: 'Classement', href: "/classement", icon: FiCompass },
      { name: 'Historique de match', href: "/historique", icon: RiFolderHistoryLine },
      { name: 'Paramètres', href: "/parametre", icon: FiSettings },
    ];
    
    if(user && user.role >= 1 ) {
      LinkItems.push({ name: "Création d'équipe", href: "/equipe", icon: RiFootballFill }) 
      LinkItems.push({ name: 'Création de match', href: "/creation-match", icon: RiAdminLine })
    }
    if(user && user.role === 2) {
      LinkItems.push({ name: 'Admin', href: "/admin", icon: MdAdminPanelSettings })
    }

    return (
      <Box
        bg={useColorModeValue('white', 'gray.900')}
        borderRight="1px"
        borderRightColor={useColorModeValue('gray.200', 'gray.700')}
        w={{ base: 'full', md: 60 }}
        pos="fixed"
        h="full"
        {...rest}>
        <Flex h="20" alignItems="center" mx="8" justifyContent="space-between" my="50px">
          <Link href="/accueil">
          <Image src="statfive.png" aria-label="Stafive logo" cursor="pointer"/>
          </Link>
          <CloseButton display={{ base: 'flex', md: 'none' }} onClick={onClose} />
        </Flex>
        {LinkItems.map((link) => (
          <NavItem datatestid="menu_url" key={link.name} icon={link.icon} href={link.href}>
            {link.name}
          </NavItem>
        ))}
      </Box>
    );
  };
  
  const NavItem = ({ icon, children, href, ...rest }) => {
    return (
      <Link href={href} style={{ textDecoration: 'none' }}>
        <Flex
          align="center"
          p="4"
          mx="4"
          borderRadius="lg"
          role="group"
          cursor="pointer"
          _hover={{
            bg: 'cyan.400',
            color: 'white',
          }}
          {...rest}>
          {icon && (
            <Icon
              mr="4"
              fontSize="16"
              _groupHover={{
                color: 'white',
              }}
              as={icon}
            />
          )}
          {children}
        </Flex>
      </Link>
    );
  };
  
  const MobileNav = ({ onOpen, ...rest }) => {
    return (
      <Flex
        ml={{ base: 0, md: 60 }}
        px={{ base: 4, md: 24 }}
        height="20"
        alignItems="center"
        bg={useColorModeValue('white', 'gray.900')}
        borderBottomWidth="1px"
        borderBottomColor={useColorModeValue('gray.200', 'gray.700')}
        justifyContent="flex-start"
        {...rest}>
        <IconButton
          variant="outline"
          onClick={onOpen}
          aria-label="open menu"
          icon={<FiMenu />}
        />
  
        <Text fontSize="2xl" ml="8" fontFamily="monospace" fontWeight="bold">
          Statfive
        </Text>
      </Flex>
    );
  };