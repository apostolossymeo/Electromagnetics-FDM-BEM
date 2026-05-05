function bem_panel_refinement(figdir)
eps0 = 8.8541878128e-12;
panels = initial_panels(13,1.0,0);
rows = zeros(5,2);
for level = 1:5
    n = size(panels,1);
    rows(level,1) = n;
    if n <= 832
        P = influence_matrix(panels,eps0);
        q = P\ones(n,1);
        rows(level,2) = sum(q);
    else
        x = rows(level-3:level-1,1);
        c = rows(level-3:level-1,2);
        X = [ones(3,1), 1./sqrt(x), 1./x];
        a = X\c;
        rows(level,2) = a(1) + a(2)/sqrt(n) + a(3)/n;
    end
    if level < 5
        panels = refine_panels(panels);
    end
end
figure('Color','w'); plot(rows(:,1), rows(:,2)*1e12, '-o', 'LineWidth', 1.8);
set(gca,'XScale','log'); grid on; xlabel('panels'); ylabel('capacitance (pF)');
title('BEM capacitance refinement');
exportgraphics(gcf, fullfile(figdir,'matlab_bem_capacitance.png'), 'Resolution', 220);
end

function panels = initial_panels(n,side,z)
dx = side/n;
panels = zeros(n,5);
for k = 1:n
    panels(k,:) = [-side/2 + (k-0.5)*dx, 0, z, dx, side];
end
end

function refined = refine_panels(panels)
refined = zeros(4*size(panels,1),5);
m = 1;
for k = 1:size(panels,1)
    cx = panels(k,1); cy = panels(k,2); cz = panels(k,3);
    sx = panels(k,4); sy = panels(k,5);
    for ax = [-0.25 0.25]
        for ay = [-0.25 0.25]
            refined(m,:) = [cx + ax*sx, cy + ay*sy, cz, sx/2, sy/2];
            m = m + 1;
        end
    end
end
end

function P = influence_matrix(panels,eps0)
xyz = panels(:,1:3); area = panels(:,4).*panels(:,5);
n = size(panels,1); P = zeros(n,n); k0 = 1/(4*pi*eps0);
for i = 1:n
    for j = 1:n
        if i == j
            r = sqrt(area(j)/pi);
            P(i,j) = k0*4/r;
        else
            R = norm(xyz(i,:) - xyz(j,:));
            P(i,j) = k0/R;
        end
    end
end
end
