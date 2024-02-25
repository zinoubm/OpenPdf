import PropTypes from 'prop-types';
import { useRef, useState, useEffect } from 'react';
import useAuth from 'api/hooks/useAuth';
import useApi from 'api/hooks/useApi';
import { useSelector, useDispatch } from 'react-redux';

import { activeUserEmail, activeUserFullName, activeUserId } from 'store/reducers/auth';

import { useTheme } from '@mui/material/styles';
import { Box, ButtonBase, CardContent, ClickAwayListener, Grid, Paper, Popper, Stack, Typography } from '@mui/material';

import MainCard from 'components/MainCard';
import { Button, Progress, Badge, Input, Space } from 'antd';

import Transitions from 'components/@extended/Transitions';
import { LogoutOutlined, ArrowRightOutlined } from '@ant-design/icons';

const computeUsagePercentage = (usage, limit) => {
  return (parseInt(usage) / parseInt(limit)) * 100;
};

function TabPanel({ children, value, index, ...other }) {
  return (
    <div role="tabpanel" hidden={value !== index} id={`profile-tabpanel-${index}`} aria-labelledby={`profile-tab-${index}`} {...other}>
      {value === index && children}
    </div>
  );
}

TabPanel.propTypes = {
  children: PropTypes.node,
  index: PropTypes.any.isRequired,
  value: PropTypes.any.isRequired
};

const Profile = () => {
  const theme = useTheme();
  const { userFullName, userEmail } = useSelector((state) => state.auth);
  const { paymentSummary } = useSelector((state) => state.app);

  const dispatch = useDispatch();

  const { deleteToken } = useAuth();
  const { currentUser } = useApi();

  const handleLogout = async () => {
    deleteToken();
  };

  const anchorRef = useRef(null);
  const [open, setOpen] = useState(false);
  const handleToggle = () => {
    setOpen((prevOpen) => !prevOpen);
  };

  const handleClose = (event) => {
    if (anchorRef.current && anchorRef.current.contains(event.target)) {
      return;
    }
    setOpen(false);
  };

  const getInitials = (fullName) => {
    return fullName[0].toUpperCase();
  };

  useEffect(() => {
    const getCurrentUser = async (dispatch) => {
      const response = await currentUser();
      if (response.success) {
        dispatch(activeUserEmail({ userEmail: response.data.email }));
        dispatch(activeUserFullName({ userFullName: response.data.full_name }));
        dispatch(activeUserId({ userId: response.data.id }));
      }
    };
    getCurrentUser(dispatch);
  }, []);

  const iconBackColorOpen = 'grey.300';

  return (
    <Box sx={{ flexShrink: 0, ml: 0.75 }}>
      <ButtonBase
        sx={{
          p: 0.25,
          bgcolor: open ? iconBackColorOpen : 'transparent',
          borderRadius: 1,
          '&:hover': { bgcolor: 'secondary.lighter' }
        }}
        aria-label="open profile"
        ref={anchorRef}
        aria-controls={open ? 'profile-grow' : undefined}
        aria-haspopup="true"
        onClick={handleToggle}
      >
        <Stack direction="row" spacing={2} alignItems="center" sx={{ p: 0.5 }}>
          <div
            style={{
              backgroundColor: '#0a0a0a',
              width: '48px',
              height: '48px',
              borderRadius: '50%',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: 'white',
              fontWeight: 'bold',
              fontSize: '20px'
            }}
          >
            {getInitials(userFullName)}
          </div>
        </Stack>
      </ButtonBase>
      <Popper
        placement="bottom-end"
        open={open}
        anchorEl={anchorRef.current}
        role={undefined}
        transition
        disablePortal
        popperOptions={{
          modifiers: [
            {
              name: 'offset',
              options: {
                offset: [0, 9]
              }
            }
          ]
        }}
      >
        {({ TransitionProps }) => (
          <Transitions type="fade" in={open} {...TransitionProps}>
            {open && (
              <Paper
                sx={{
                  boxShadow: theme.customShadows.z1,
                  width: 290,
                  minWidth: 320,
                  maxWidth: 400,
                  [theme.breakpoints.down('md')]: {
                    maxWidth: 250
                  }
                }}
              >
                <ClickAwayListener onClickAway={handleClose}>
                  <MainCard elevation={0} border={false} content={false}>
                    <CardContent sx={{ px: 2.5, pt: 3 }}>
                      <Grid container justifyContent="space-between" alignItems="center">
                        <Grid item>
                          <Stack direction="row" spacing={1.25} alignItems="center">
                            <div
                              style={{
                                backgroundColor: '#0a0a0a',
                                width: '48px',
                                height: '48px',
                                borderRadius: '50%',
                                display: 'flex',
                                alignItems: 'center',
                                justifyContent: 'center',
                                color: 'white',
                                fontWeight: 'bold',
                                fontSize: '20px'
                              }}
                            >
                              {getInitials(userFullName)}
                            </div>
                            <Stack>
                              <Typography variant="h6">{userFullName}</Typography>
                              <Typography variant="body2" color="textSecondary">
                                {userEmail}
                              </Typography>
                            </Stack>
                          </Stack>
                          {paymentSummary && (
                            <div style={{ margin: '1em 0em' }}>
                              <div style={{ display: 'flex', flexDirection: 'row', justifyContent: 'space-between' }}>
                                <Typography variant="h6">Plan: {paymentSummary.plan} </Typography>
                                <Badge
                                  style={{ backgroundColor: paymentSummary.plan_status === 'ACTIVE' ? '#0ec295' : '#ff2448' }}
                                  count={paymentSummary.plan_status}
                                ></Badge>
                              </div>

                              <Typography variant="h6">Usage</Typography>
                              <Typography variant="body2" color="textSecondary">
                                Uploads: {paymentSummary.usage.UPLOADS}/{paymentSummary.user_limits.UPLOADS}
                              </Typography>
                              <Progress
                                percent={computeUsagePercentage(paymentSummary.usage.UPLOADS, paymentSummary.user_limits.UPLOADS)}
                                showInfo={false}
                                size={[240, 10]}
                              />
                              <Typography variant="body2" color="textSecondary">
                                Questions: {paymentSummary.usage.QUERIES}/{paymentSummary.user_limits.QUERIES}
                              </Typography>
                              <Progress
                                percent={computeUsagePercentage(paymentSummary.usage.QUERIES, paymentSummary.user_limits.QUERIES)}
                                showInfo={false}
                                size={[240, 10]}
                              />
                            </div>
                          )}
                        </Grid>
                        <Grid item>
                          <Space.Compact style={{ width: '100%', margin: '12px 0' }}>
                            <Input placeholder="xxxx-xxxx-xxxx-xxxx" />
                            <Button type="primary">
                              <ArrowRightOutlined />
                            </Button>
                          </Space.Compact>

                          <Button icon={<LogoutOutlined />} onClick={handleLogout}>
                            Logout
                          </Button>
                        </Grid>
                      </Grid>
                    </CardContent>
                    {open && (
                      <>
                        <Box sx={{ borderBottom: 1, borderColor: 'divider' }}></Box>
                      </>
                    )}
                  </MainCard>
                </ClickAwayListener>
              </Paper>
            )}
          </Transitions>
        )}
      </Popper>
    </Box>
  );
};

export default Profile;
