function fdm_sparse_electrostatics(figdir)
N = 120; Lx = 4; Ly = 4; V0 = 100;
x = linspace(0,Lx,N); y = linspace(0,Ly,N);
hx = x(2)-x(1); hy = y(2)-y(1);
nx = N-2; ny = N-2; M = nx*ny;
idx = @(i,j) (i-1)*ny + j;
A = spalloc(M,M,5*M); b = zeros(M,1);
cx = 1/hx^2; cy = 1/hy^2;
for i = 1:nx
    for j = 1:ny
        k = idx(i,j);
        A(k,k) = -2*(cx+cy);
        if i > 1, A(k,idx(i-1,j)) = cx; end
        if i < nx, A(k,idx(i+1,j)) = cx; end
        if j > 1, A(k,idx(i,j-1)) = cy; end
        if j < ny
            A(k,idx(i,j+1)) = cy;
        else
            b(k) = b(k) - cy*V0;
        end
    end
end
v = A\b;
V = zeros(N,N); V(:,end) = V0;
for i = 1:nx
    for j = 1:ny
        V(i+1,j+1) = v(idx(i,j));
    end
end
[X,Y] = meshgrid(x,y);
figure('Color','w'); spy(A); title('Sparse FDM operator'); xlabel('column'); ylabel('row');
exportgraphics(gcf, fullfile(figdir,'matlab_sparse_operator.png'), 'Resolution', 220);
figure('Color','w'); contourf(X,Y,V',24,'LineColor','none'); axis equal tight; colorbar;
title('MATLAB sparse FDM potential'); xlabel('x'); ylabel('y');
exportgraphics(gcf, fullfile(figdir,'matlab_fdm_potential.png'), 'Resolution', 220);
end
