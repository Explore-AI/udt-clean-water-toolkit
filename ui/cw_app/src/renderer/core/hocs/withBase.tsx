import usePortal, { PortalContext } from "../hooks/usePortal";
import useEsriGisAuth from "../hooks/useEsriGisAuth";
import useUi, { UiContext } from "../hooks/useUi";
import { UserContext } from "../controllers/UserController";
import useGetUserData from "../hooks/useGetUserData";
import { isEmpty } from "lodash";

const withBase = (PageComponent) => {
  const HOC = (props) => {
    const user = useGetUserData();
    const redirect_url = "/map";
    const isValidUser  = !isEmpty(user) ? true : false

    const { isGisAuthValid, isRedirectUrlSet } = useEsriGisAuth(
      isValidUser,
      redirect_url
    );
    const { uiParams, setUiParams } = useUi();

    const portalValues = usePortal();
    if (isGisAuthValid && isRedirectUrlSet) {
      return (
        <UserContext.Provider
          value={{ user: user, is_gis_auth_valid: isGisAuthValid }}
        >
          <PortalContext.Provider value={portalValues}>
            <UiContext.Provider value={{ uiParams, setUiParams }}>
              <PageComponent {...props} />
            </UiContext.Provider>
          </PortalContext.Provider>
        </UserContext.Provider>
      );
    }
    return null;
  };

  return HOC;
};

export default withBase;
