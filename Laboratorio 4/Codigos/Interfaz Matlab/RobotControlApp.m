function varargout = RobotControlApp(varargin)
% ROBOTCONTROLAPP MATLAB code for RobotControlApp.fig
%      ROBOTCONTROLAPP, by itself, creates a new ROBOTCONTROLAPP or raises the existing
%      singleton*.
%
%      H = ROBOTCONTROLAPP returns the handle to a new ROBOTCONTROLAPP or the handle to
%      the existing singleton*.
%
%      ROBOTCONTROLAPP('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in ROBOTCONTROLAPP.M with the given input arguments.
%
%      ROBOTCONTROLAPP('Property','Value',...) creates a new ROBOTCONTROLAPP or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before RobotControlApp_OpeningFcn gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to RobotControlApp_OpeningFcn via varargin.
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help RobotControlApp

% Last Modified by GUIDE v2.5 27-May-2024 12:00:00

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @RobotControlApp_OpeningFcn, ...
                   'gui_OutputFcn',  @RobotControlApp_OutputFcn, ...
                   'gui_LayoutFcn',  [] , ...
                   'gui_Callback',   []);
if nargin && ischar(varargin{1})
    gui_State.gui_Callback = str2func(varargin{1});
end

if nargout
    [varargout{1:nargout}] = gui_mainfcn(gui_State, varargin{:});
else
    gui_mainfcn(gui_State, varargin{:});
end
% End initialization code - DO NOT EDIT

% --- Executes just before RobotControlApp is made visible.
function RobotControlApp_OpeningFcn(hObject, eventdata, handles, varargin)
% Choose default command line output for RobotControlApp
handles.output = hObject;

% Update handles structure
guidata(hObject, handles);

% Define poses
handles.poses = {
    [0, 0, 0, 0, 0], ...
    [25, 25, 20, -20, 0], ...
    [-35, 35, -30, 30, 0], ...
    [85, -20, 55, 25, 0], ...
    [80, -35, 55, -45, 0]
};

% Initializa pose robot y logo
axes(handles.axeslogo);
imshow(imread('logounal.jpg'), 'Parent', handles.axeslogo, 'InitialMagnification', 'fit');

% --- Executes on selection change in popupmenuPose.
function popupmenuPose_Callback(hObject, eventdata, handles)
coord=get(hObject,'String');
indice = get(hObject, 'Value');
handles.selectedPose=coord{indice}
set(handles.coord, 'String', handles.selectedPose)
guidata(hObject, handles);
% --- Executes during object creation, after setting all properties.
function popupmenuPose_CreateFcn(hObject, eventdata, handles)
% If using Windows, set background color to white
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end

% --- Executes on button press in EnviarPush.
function EnviarPush_Callback(hObject, eventdata, handles)
handles = guidata(hObject); % Recupera la estructura handles actualizada
ang = str2num(handles.selectedPose) % Cadena a un vector numérico

l = [14.5, 10.5, 10.55, 9.1]; % Longitudes eslabones [mm]
% Definicion del robot RTB
L(1) = Link('revolute','alpha',-pi/2, 'a',0,    'd',l(1), 'offset',0,     'qlim',[-3*pi/4 3*pi/4]);
L(2) = Link('revolute','alpha',0,     'a',l(2), 'd',0,    'offset',-pi/2, 'qlim',[-3*pi/4 3*pi/4]);
L(3) = Link('revolute','alpha',0,     'a',l(3), 'd',0,    'offset',0,  'qlim',[-3*pi/4 3*pi/4]);
L(4) = Link('revolute','alpha',0,     'a',l(4), 'd',0,    'offset',0,     'qlim',[-3*pi/4 3*pi/4]);
PhantomX = SerialLink(L,'name','Px');
% roty(pi/2)*rotz(-pi/2)
PhantomX.tool = [1 0 0 l(4); 0 1 0 0; 0 0 1 0; 0 0 0 1];

if ang== [0, 0, 0, 0, 0]
    angf= [0,0,0,0]
elseif ang == [25, 25, 20, -20, 0]
    angf= [25,25,20,-20]
elseif ang == [-35, 35, -30, 30, 0]
    angf= [-35, 35, -30, 30]
elseif ang== [85, -20, 55, 25, 0]
    angf= [85, -20, 55, 25]
elseif ang ==[80, -35, 55, -45, 0]
    angf=[80, -35, 55, -45]
end

% Intentar abrir el archivo para escritura
fileID = fopen('~/Escritorio/Robotica/jointData.txt', 'w');

% Escribir los datos del vector en el archivo
fprintf(fileID, '%f\n', ang);

% Cerrar el archivo
fclose(fileID);
% Actualizar grafico pose
axes(handles.axesCurrentPose);
PhantomX.plot(angf)
