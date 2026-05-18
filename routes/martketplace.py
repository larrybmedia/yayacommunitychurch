@app.route('/marketplace')
def marketplace():
    # 1. Get the current branch from the session
    active_branch_id = session.get('selected_branch_id')
    
    # 2. Get all branches for the dropdown menu in base.html
    branches = Branch.query.all()
    
    if active_branch_id:
        # Get businesses for the selected branch
        local_businesses = Business.query.filter_by(branch_id=active_branch_id).all()
        
        # Get businesses from ALL OTHER branches (Optional: to fill up the page)
        other_businesses = Business.query.filter(Business.branch_id != active_branch_id).all()
        
        return render_template('marketplace.html', 
                               local_biz=local_businesses, 
                               other_biz=other_businesses, 
                               branches=branches)
    
    # 3. If no branch is selected, show everyone as "All Businesses"
    all_businesses = Business.query.all()
    return render_template('marketplace.html', 
                           local_biz=all_businesses, 
                           other_biz=[], 
                           branches=branches)

return render_template('index.html', 
                       global_posts=global_posts, 
                       local_posts=local_posts, 
                       stream=local_stream, 
                       branches=branches)