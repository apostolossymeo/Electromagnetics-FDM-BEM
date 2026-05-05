clear; clc; close all;
rootdir = fileparts(fileparts(fileparts(mfilename('fullpath'))));
figdir = fullfile(rootdir,'figures','matlab');
if ~exist(figdir,'dir')
    mkdir(figdir);
end
fdm_sparse_electrostatics(figdir);
bem_panel_refinement(figdir);
