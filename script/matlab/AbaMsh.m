% This script converts .inp file which are output of ANSA and coverts it
% into .msh file.
%
% The file has to be in the same folder of this script or you need to
% specify the full path. The .inp file has to be an Abaqus output of ANSA 
% and must contains nodes and elements only.
%
% OUTPUT: new folder containing .msh file


curfile = "C:\Users\Veronica\Desktop\PhD\FuTURO\mesh\2CONNECTEDLAYERS\ANSA\muscle_linked_nodes.inp";
% open file
ID_in = fopen(curfile, 'r');

while ~ strcmp(fgetl(ID_in), '*NODE')
    % do nothing
end
nodesFormat='%d, %f, %f, %f'; 
nodes = textscan(ID_in, nodesFormat); %leggo nodi
nodesCoord = [nodes{2}, nodes{3}, nodes{4}];
n_nodes = size(nodesCoord, 1);

% cerco dove iniziano gli elementi
pattern = '*ELEMENT,';
curline = fgetl(ID_in);
while ~ contains(curline, pattern)
    % skip line
    curline = fgetl(ID_in); % line update
end
disp(curline) % just to check everything is fine
elemFormat = '%d, %d, %d, %d, %d';
elem = cell2mat(textscan(ID_in, elemFormat));
n_el = size(elem,1);

fclose(ID_in);
%% Write .msh file
mesh_name = erase(curfile,'.inp');
file_msh = strcat(mesh_name, '.msh');
mkdir(mesh_name);
% print header and nodes
ID_out = fopen(file_msh, 'w');
fprintf(ID_out, "$MeshFormat\n2.2 0 8\n$EndMeshFormat\n$Nodes\n%i\n", n_nodes);
for i = 1:n_nodes
    fprintf(ID_out, '%d  %f  %f  %f\n', nodes{1,1}(i), nodesCoord(i, 1:3));
end

fprintf(ID_out,"$EndNodes\n$Elements\n%i\n", n_el);

% print elements
for i=1:n_el
    fprintf(ID_out, '%i 4 2 0 1 %i %i %i %i\n', elem(i,:));
end
fprintf(ID_out, "$EndElements");
fclose(ID_out);

movefile(file_msh, mesh_name);
movefile(strcat(mesh_name, '.inp'), mesh_name)

